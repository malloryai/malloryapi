"""Check SDK route and parameter coverage without sending network requests.

Run: python scripts/check_openapi.py [--schema path/to/openapi.json]
The default fixture is a compact snapshot of the public API, captured 2026-09-11.
This checks transport contracts, not server-side validation of payload values.
"""

from __future__ import annotations

import argparse
import asyncio
import inspect
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from malloryapi import AsyncMalloryApi, MalloryApi  # noqa: E402

DEFAULT_SCHEMA = ROOT / "tests" / "fixtures" / "openapi_contract.json"
VERBS = {"get", "post", "patch", "put", "delete"}


def resolve(schema: dict, spec: dict) -> dict:
    if "$ref" in schema:
        return spec["components"]["schemas"][schema["$ref"].rsplit("/", 1)[1]]
    return schema


def sample(schema: dict, spec: dict, depth: int = 0) -> Any:
    """Representative transport values; not a general JSON Schema generator."""
    schema = resolve(schema, spec)
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        return schema["enum"][-1]
    for union in ("anyOf", "oneOf"):
        if union in schema:
            return sample(
                next(s for s in schema[union] if s.get("type") != "null"), spec, depth
            )
    kind = schema.get("type")
    if kind == "boolean":
        return not schema.get("default", False)
    if kind in ("integer", "number"):
        return max(
            schema.get("minimum", 0),
            min(
                7,
                schema.get("maximum", 100) - 1,
                schema.get("exclusiveMaximum", 100) - 1,
            ),
        )
    if kind == "array":
        return (
            [sample(schema.get("items", {}), spec, depth + 1)] * 2 if depth < 4 else []
        )
    if kind == "object" or "properties" in schema:
        if depth >= 4:
            return {}
        return {
            key: sample(value, spec, depth + 1)
            for key, value in schema.get("properties", {}).items()
        }
    if schema.get("format") == "date-time":
        return "2026-09-11T12:34:56Z"
    if schema.get("format") == "uuid":
        return "11111111-1111-4111-8111-111111111111"
    pattern = schema.get("pattern", "")
    if pattern.startswith("^(") and pattern.endswith(")$"):
        return pattern[2:-2].split("|")[-1]
    return "audit value +&"


def required_args(fn: Any) -> dict:
    args = {}
    for name, param in inspect.signature(fn).parameters.items():
        if param.default is not param.empty or param.kind in (
            param.VAR_KEYWORD,
            param.VAR_POSITIONAL,
        ):
            continue
        annotation = str(param.annotation)
        args[name] = (
            []
            if annotation.startswith("list")
            else {}
            if "dict" in annotation
            else "AUDIT" + name.upper()
        )
    return args


def normalize(path: str) -> str:
    return re.sub(r"AUDIT[A-Z_]+|\{[^}]+\}", "{}", path)


def operations(spec: dict) -> dict:
    return {
        (method.upper(), path): op
        for path, methods in spec["paths"].items()
        for method, op in methods.items()
        if method in VERBS
    }


def json_body(operation: dict) -> dict | None:
    return (
        operation.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )


def field_values(schema: dict, spec: dict) -> list:
    """Exercise nullable values and both booleans as well as the sample value."""
    schema = resolve(schema, spec)
    value = sample(schema, spec)
    values = [value]
    if isinstance(value, bool):
        values.append(not value)
    if any(s.get("type") == "null" for s in schema.get("anyOf", [])):
        values.append(None)
    return values


@dataclass
class BoundMethod:
    name: str
    call: Any
    arguments: dict
    baseline: httpx.Request


async def invoke(fn: Any, args: dict, captured: list) -> tuple:
    captured.clear()
    error = ""
    try:
        value = fn(**args)
        if inspect.isawaitable(value):
            await value
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    if len(captured) != 1:
        error = f"expected one request, got {len(captured)}; {error}"
    return (captured[-1] if captured else None), error


async def probe(method: BoundMethod, arguments: dict, captured: list) -> tuple:
    request, error = await invoke(
        method.call, {**method.arguments, **arguments}, captured
    )
    if request is None:
        return request, error or "no request sent"
    if (request.method, request.url.path) != (
        method.baseline.method,
        method.baseline.url.path,
    ):
        error = f"unexpected route {request.method} {request.url.path}; {error}"
    return request, error


async def discover_methods(client: Any, expected: dict, captured: list) -> tuple:
    """Match outgoing baseline requests to public operations; retain legacy methods."""
    routes = {(verb, normalize(path)): (verb, path) for verb, path in expected}
    covered, issues = {}, []
    resources = [("client", client)] + [
        (name, obj) for name, obj in vars(client).items() if not name.startswith("_")
    ]
    for resource, obj in resources:
        for name, fn in inspect.getmembers(obj, inspect.ismethod):
            if name.startswith("_") or name in {
                "close",
                "aclose",
                "trending",
                "exploited",
                "whoami",
            }:
                continue
            method_name = f"{resource}.{name}"
            arguments = required_args(fn)
            request, error = await invoke(fn, arguments, captured)
            if request is None:
                issues.append(f"{method_name}: cannot build request: {error}")
                continue
            key = routes.get((request.method, normalize(request.url.path)))
            if key is not None:
                if error:
                    issues.append(f"{method_name}: {error}")
                covered.setdefault(
                    key, BoundMethod(method_name, fn, arguments, request)
                )
    return covered, issues


async def check_path_parameter(
    method: BoundMethod, key: tuple, name: str, captured: list
) -> list[str]:
    index = key[1].split("/").index("{" + name + "}")
    sentinel = method.baseline.url.path.split("/")[index]
    argument = next(
        (arg for arg, value in method.arguments.items() if value == sentinel), None
    )
    if argument is None:
        return [f"{' '.join(key)}: path parameter {name} not substituted"]

    value = f"{name}/audit ?#%+é"
    path, separator, query = method.baseline.url.raw_path.partition(b"?")
    segments = path.split(b"/")
    segments[index] = quote(value, safe="").encode("ascii")
    expected_path = b"/".join(segments) + separator + query
    request, error = await invoke(
        method.call, {**method.arguments, argument: value}, captured
    )
    actual = (request.method, request.url.raw_path) if request else None
    if error or actual != (method.baseline.method, expected_path):
        return [
            f"{method.name}: path parameter {name} not escaped independently: "
            f"expected {expected_path!r}, got {actual!r}; {error}"
        ]
    return []


async def check_parameters(
    method: BoundMethod, key: tuple, operation: dict, spec: dict, captured: list
) -> list[str]:
    issues = []
    for param in operation.get("parameters", []):
        name = param["name"]
        if param["in"] == "path":
            issues.extend(await check_path_parameter(method, key, name, captured))
        elif param["in"] == "query":
            for value in field_values(param["schema"], spec):
                request, error = await probe(method, {name: value}, captured)
                actual = request.url.params.get_list(name) if request else []
                expected = (
                    httpx.QueryParams({name: value}).get_list(name)
                    if value is not None
                    else []
                )
                # Require supplied values on the wire even when they equal a default:
                # otherwise a wrapper dropping that parameter can falsely pass.
                if error or actual != expected:
                    issues.append(
                        f"{method.name}: query {name}={value!r}: "
                        f"expected {expected!r}, got {actual!r}; {error}"
                    )
        else:
            issues.append(
                f"{' '.join(key)}: unchecked parameter location {param['in']}"
            )
    return issues


def body_cases(fn: Any, root: dict, spec: dict):
    """Yield keyword arguments and the JSON fields that must survive each probe."""
    signature = inspect.signature(fn)
    body_arg = next(
        (
            name
            for name in ("data", "query")
            if name in signature.parameters
            and "dict" in str(signature.parameters[name].annotation)
        ),
        None,
    )
    root = resolve(root, spec)
    for variant in root.get("oneOf", [root]):
        schema = resolve(variant, spec)
        if "anyOf" in schema:
            schema = resolve(
                next(s for s in schema["anyOf"] if s.get("type") != "null"), spec
            )
        fields = schema.get("properties", {})
        if not fields and body_arg:
            payload = {"nested": {"values": [False, 0, None]}}
            yield {body_arg: payload}, payload, "arbitrary JSON body", True
        for name, field in fields.items():
            for value in field_values(field, spec):
                field_payload = {name: value}
                arguments = (
                    {body_arg: {**sample(schema, spec), **field_payload}}
                    if body_arg
                    else field_payload
                )
                yield arguments, field_payload, f"JSON field {name}", False


async def check_body(
    method: BoundMethod, schema: dict, spec: dict, captured: list
) -> list[str]:
    issues = []
    for arguments, expected, label, whole_body in body_cases(method.call, schema, spec):
        request, error = await probe(method, arguments, captured)
        try:
            actual = (
                json.loads(request.content) if request and request.content else None
            )
        except ValueError as exc:
            actual, error = None, f"invalid JSON: {exc}"
        actual_fields = actual
        if not whole_body:
            actual_fields = (
                {name: actual[name] for name in expected if name in actual}
                if isinstance(actual, dict)
                else None
            )
        # JSON comparison also distinguishes nested booleans from 0/1, unlike ==.
        if error or json.dumps(actual_fields, sort_keys=True) != json.dumps(
            expected, sort_keys=True
        ):
            issues.append(f"{method.name}: {label} not preserved; {error}")
    return issues


async def check_client(spec: dict, client_cls: type) -> dict:
    expected = operations(spec)
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            200,
            json={
                "data": [],
                "items": [],
                "total": 0,
                "offset": 0,
                "limit": 100,
                "resolution": {"status": "unresolved"},
                "normalized_request": None,
                "mode": "configuration_match",
                "coverage": {},
            },
        )

    client = client_cls(
        api_key="offline-contract-check", transport=httpx.MockTransport(handler)
    )
    try:
        covered, issues = await discover_methods(client, expected, captured)
        for key, operation in expected.items():
            if key not in covered:
                issues.append(f"Missing operation: {' '.join(key)}")
                continue
            method = covered[key]
            issues.extend(
                await check_parameters(method, key, operation, spec, captured)
            )
            body = json_body(operation)
            if body is not None:
                issues.extend(await check_body(method, body, spec, captured))
    finally:
        if hasattr(client, "aclose"):
            await client.aclose()
        else:
            client.close()

    parameters = [
        param for key in covered for param in expected[key].get("parameters", [])
    ]
    return {
        "client": client_cls.__name__,
        "operations": len(covered),
        "query_parameters": sum(param["in"] == "query" for param in parameters),
        "path_parameters": sum(param["in"] == "path" for param in parameters),
        "body_contracts": sum(json_body(expected[key]) is not None for key in covered),
        "issues": issues,
    }


async def check_contract(spec: dict) -> list[dict]:
    return [await check_client(spec, cls) for cls in (MalloryApi, AsyncMalloryApi)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()
    results = asyncio.run(check_contract(json.loads(args.schema.read_text())))
    print(json.dumps(results, indent=2))
    return int(any(result["issues"] for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
