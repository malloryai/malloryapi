"""Command-line interface for the Mallory API.

Enables agents and users to call the API via shell:

    malloryapi vulnerabilities get CVE-2024-1234
    malloryapi threat_actors trending --period 7d --limit 10
    malloryapi search query --q "APT28"
"""

from __future__ import annotations

import argparse
import inspect
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import httpx

# Resource name (as used in CLI) -> MalloryApi attribute name
RESOURCE_ALIASES: dict[str, str] = {
    "vulns": "vulnerabilities",
    "actors": "threat_actors",
    "orgs": "organizations",
    "chunks": "content_chunks",
    "sigs": "detection_signatures",
    "aps": "attack_patterns",
    "pkgs": "packages",
    "geo": "geographies",
}

# All MalloryApi resource attributes (sync client)
RESOURCE_NAMES = [
    "vulnerabilities",
    "threat_actors",
    "malware",
    "exploits",
    "exploitations",
    "organizations",
    "products",
    "attack_patterns",
    "breaches",
    "detection_signatures",
    "detections",
    "malware_samples",
    "malware_sample_analyses",
    "malware_sample_reports",
    "advisories",
    "weaknesses",
    "stories",
    "references",
    "sources",
    "content_chunks",
    "observables",
    "opinions",
    "mentions",
    "search",
    "dashboards",
    "industries",
    "schedules",
    "workspaces",
    "exports",
    "integrations",
    "vulnerable_configurations",
    "assets",
    "packages",
    "extensions",
    "geographies",
    "tenants",
    "findings",
    "finding_definitions",
    "profiles",
    "sightings",
    "vtpcs",
    "user",
]


def _resolve_resource_name(name: str) -> str:
    """Resolve CLI resource name (including alias) to MalloryApi attribute."""
    key = name.lower().strip()
    return RESOURCE_ALIASES.get(key, key)


def _get_public_methods(obj: Any) -> list[str]:
    """Return public method names of obj (no _ prefix)."""
    return [m for m in dir(obj) if not m.startswith("_") and callable(getattr(obj, m))]


def _write_error(msg: str, status_code: int | None = None) -> None:
    """Write JSON error to stderr for agent parsing."""
    payload: dict[str, Any] = {"error": msg}
    if status_code is not None:
        payload["status_code"] = status_code
    sys.stderr.write(json.dumps(payload) + "\n")


def _serialize_result(result: Any) -> Any:
    """Convert SDK result to JSON-serializable structure."""
    if is_dataclass(result) and not isinstance(result, type):
        payload = asdict(result)
        if hasattr(result, "has_more"):
            payload["has_more"] = result.has_more
        return payload
    if hasattr(result, "items") and hasattr(result, "total"):
        return {
            "total": getattr(result, "total", None),
            "offset": getattr(result, "offset", None),
            "limit": getattr(result, "limit", None),
            "has_more": getattr(result, "has_more", None),
            "items": list(result),
        }
    if result is None or isinstance(result, (dict, list, str, int, float, bool)):
        return result
    return str(result)


# Parameters fed by named flags (e.g. --q, --urls) rather than the
# positional identifier; methods whose first arg is one of these are
# dispatched via kwargs, not the positional identifier.
_FLAG_BACKED_PARAMS = frozenset(
    {"q", "urls", "types", "limit", "offset", "sort", "order", "filter", "period"}
)


def _positional_params(fn: Any, supplied: set[str]) -> list[inspect.Parameter]:
    """Return the positional parameters the CLI must bind for ``fn``.

    Skips ``self``, parameters fed by named flags, and any parameter already
    supplied via kwargs. Both required and optional positionals are returned,
    in declaration order, so the dispatcher can bind CLI positionals to methods
    that take more than one (e.g. ``update_member(uuid, user_uuid, data)``).
    This is name-agnostic so it works regardless of the parameter's name
    (``identifier``, ``code``, ``tenant_uuid``, ``entity_type``, etc.).
    """
    params: list[inspect.Parameter] = []
    for name, p in inspect.signature(fn).parameters.items():
        if name == "self" or name in _FLAG_BACKED_PARAMS or name in supplied:
            continue
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD):
            params.append(p)
    return params


def main(
    argv: list[str] | None = None, *, transport: httpx.BaseTransport | None = None
) -> int:
    """Run the CLI with optional arguments and an injectable HTTP boundary."""
    try:
        from malloryapi import MalloryApi  # noqa: E402
    except ImportError:
        _write_error("malloryapi is not installed. Run: pip install malloryapi")
        return 1

    parser = argparse.ArgumentParser(
        prog="malloryapi",
        description="Mallory Threat Intelligence API CLI (agents and shell)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  malloryapi vulnerabilities get CVE-2024-1234\n"
            "  malloryapi threat_actors trending --period 7d --limit 10\n"
            "  malloryapi search query --q APT28\n"
            "  malloryapi --help-resources\n"
        ),
    )
    parser.add_argument(
        "--help-resources",
        action="store_true",
        help="List all resources and their methods (for agent discovery)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key (or set MALLORY_API_KEY env var)",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="API base URL (default: https://api.mallory.ai/v1)",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Output single-line JSON",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print raw response without pagination envelope",
    )
    parser.add_argument(
        "resource",
        nargs="?",
        default=None,
        help="Resource name (e.g. vulnerabilities, threat_actors, vulns, actors)",
    )
    parser.add_argument(
        "method",
        nargs="?",
        default=None,
        help="Method to call (e.g. list, get, trending)",
    )
    parser.add_argument(
        "identifier",
        nargs="*",
        default=[],
        help=(
            "Positional argument(s) for the method: an identifier (CVE ID, "
            "UUID), plus any further positionals such as user UUID, entity "
            "type, or a JSON body for create/add/update methods"
        ),
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--offset", type=int, default=None)
    parser.add_argument("--sort", default=None)
    parser.add_argument("--order", default=None)
    parser.add_argument("--filter", default=None, dest="filter_")
    parser.add_argument("--period", default=None)
    parser.add_argument("--q", default=None, help="Search query string")
    parser.add_argument("--types", default=None, help="Search types filter")
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="Additional SDK keyword argument; JSON values preserve booleans/numbers",
    )
    parser.add_argument(
        "--urls",
        action="append",
        default=None,
        help="URLs for references create (repeat or comma-separated)",
    )

    parser.add_argument(
        "--input-file", type=Path,
        help="Read raw bytes for a method's content argument (sample uploads)",
    )
    parser.add_argument(
        "--output", type=Path,
        help="Save a binary download to this file instead of printing JSON",
    )

    args = parser.parse_args(argv)

    if args.resource is None and not args.help_resources:
        parser.print_help()
        sys.stderr.write(
            "\nUse malloryapi --help-resources to list resources and methods.\n"
        )
        return 0

    client_kw: dict[str, Any] = {
        "api_key": (args.api_key or "help") if args.help_resources else args.api_key,
        "transport": transport,
    }
    if args.base_url is not None:
        client_kw["base_url"] = args.base_url
    try:
        with MalloryApi(**client_kw) as client:
            if args.help_resources:
                return _show_resources(client)
            return _dispatch(client, args)
    except Exception as exc:
        _write_error(str(exc))
        return 1


def _show_resources(client: Any) -> int:
    out: dict[str, list[str]] = {}
    for attr in RESOURCE_NAMES:
        res = getattr(client, attr, None)
        if res is not None:
            out[attr] = _get_public_methods(res)
    aliases = [
        f"  {alias} -> {full}" for alias, full in sorted(RESOURCE_ALIASES.items())
    ]
    sys.stdout.write(
        json.dumps(
            {
                "resources": out,
                "aliases": RESOURCE_ALIASES,
                "alias_help": aliases,
            },
            indent=2,
        )
        + "\n"
    )
    return 0


def _dispatch(client: Any, args: argparse.Namespace) -> int:
    resolved = _resolve_resource_name(args.resource)
    resource = getattr(client, resolved, None)
    if resource is None:
        _write_error(
            f"Unknown resource: {args.resource}. "
            f"Available: {', '.join(RESOURCE_NAMES)}. "
            f"Aliases: {', '.join(RESOURCE_ALIASES)}."
        )
        return 1

    if args.method is None:
        methods = _get_public_methods(resource)
        _write_error(
            f"Method required for resource '{args.resource}'. "
            f"Available: {', '.join(sorted(methods))}."
        )
        return 1

    method_fn = getattr(resource, args.method, None)
    if method_fn is None:
        methods = _get_public_methods(resource)
        _write_error(
            f"Unknown method '{args.method}' on resource '{args.resource}'. "
            f"Available: {', '.join(sorted(methods))}."
        )
        return 1

    returns_bytes = str(inspect.signature(method_fn).return_annotation) == "bytes"
    if args.output is not None and not returns_bytes:
        _write_error("--output is only supported for binary downloads")
        return 1
    if returns_bytes and args.output is None:
        _write_error("Binary downloads require --output FILE")
        return 1

    kwargs = {
        name: getattr(args, name)
        for name in ("limit", "offset", "sort", "order", "period", "q", "types")
        if getattr(args, name) is not None
    }
    if args.filter_ is not None:
        kwargs["filter"] = args.filter_
    if args.urls is not None:
        urls: list[str] = []
        for u in args.urls:
            urls.extend(s.strip() for s in u.split(",") if s.strip())
        kwargs["urls"] = urls

    for entry in args.param:
        name, separator, raw = entry.partition("=")
        if not separator or not name:
            _write_error("--param requires NAME=VALUE")
            return 1
        if name in kwargs:
            _write_error(f"Argument '{name}' was supplied more than once")
            return 1
        try:
            kwargs[name] = json.loads(raw)
        except json.JSONDecodeError:
            kwargs[name] = raw

    if args.input_file is not None:
        content_param = inspect.signature(method_fn).parameters.get("content")
        if content_param is None or str(content_param.annotation) != "bytes":
            _write_error("--input-file requires a method accepting binary content")
            return 1
        if "content" in kwargs:
            _write_error("--input-file cannot be combined with --param content")
            return 1
        kwargs["content"] = args.input_file.read_bytes()

    pos_params = _positional_params(method_fn, set(kwargs))
    required = [p for p in pos_params if p.default is p.empty]
    provided = list(args.identifier)

    if len(provided) < len(required):
        if len(required) == 1:
            _write_error(f"Method '{args.method}' requires an identifier")
        else:
            names = ", ".join(p.name for p in required)
            _write_error(
                f"Method '{args.method}' requires {len(required)} "
                f"positional argument(s): {names}"
            )
        return 1

    if not required:
        if resolved == "search" and args.method == "query" and "q" not in kwargs:
            _write_error("Search query requires --q")
            return 1
        if (
            resolved == "references"
            and args.method == "create"
            and "urls" not in kwargs
        ):
            _write_error("references create requires --urls")
            return 1

    # Bind CLI positionals to the method's positional params in order,
    # JSON-decoding any value destined for a ``data`` body parameter.
    bound: list[Any] = []
    for param, raw in zip(pos_params, provided):
        value: Any = raw
        if param.name in {"data", "query"}:
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                _write_error(
                    f"Argument '{param.name}' for '{args.method}' must be valid JSON"
                )
                return 1
        if param.kind == param.POSITIONAL_ONLY:
            bound.append(value)
        else:
            kwargs[param.name] = value

    try:
        result = method_fn(*bound, **kwargs)
    except Exception as exc:
        from malloryapi.exceptions import APIError  # noqa: E402

        if isinstance(exc, APIError):
            _write_error(str(exc), getattr(exc, "status_code", None))
        else:
            _write_error(str(exc))
        return 1

    if isinstance(result, bytes):
        if args.output is None:
            _write_error("Binary downloads require --output FILE")
            return 1
        args.output.write_bytes(result)
        return 0
    if args.output is not None:
        _write_error("--output is only supported for binary downloads")
        return 1

    output = _serialize_result(result)
    if args.raw and isinstance(output, dict) and "items" in output:
        output = output.get("items", output)
    indent = None if args.compact else 2
    sys.stdout.write(json.dumps(output, indent=indent, default=str) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
