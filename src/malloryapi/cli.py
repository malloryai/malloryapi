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
from typing import Any

# Resource name (as used in CLI) -> MalloryApi attribute name
RESOURCE_ALIASES: dict[str, str] = {
    "vulns": "vulnerabilities",
    "actors": "threat_actors",
    "orgs": "organizations",
    "chunks": "content_chunks",
    "sigs": "detection_signatures",
    "aps": "attack_patterns",
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
    "advisories",
    "weaknesses",
    "stories",
    "references",
    "sources",
    "content_chunks",
    "mentions",
    "search",
]


def _resolve_resource_name(name: str) -> str:
    """Resolve CLI resource name (including alias) to MalloryApi attribute."""
    key = name.lower().strip()
    return RESOURCE_ALIASES.get(key, key)


def _get_public_methods(obj: Any) -> list[str]:
    """Return public method names of obj (no _ prefix)."""
    return [
        m
        for m in dir(obj)
        if not m.startswith("_") and callable(getattr(obj, m))
    ]


def _write_error(msg: str, status_code: int | None = None) -> None:
    """Write JSON error to stderr for agent parsing."""
    payload: dict[str, Any] = {"error": msg}
    if status_code is not None:
        payload["status_code"] = status_code
    sys.stderr.write(json.dumps(payload) + "\n")


def _serialize_result(result: Any) -> Any:
    """Convert SDK result to JSON-serializable structure."""
    if hasattr(result, "items") and hasattr(result, "total"):
        return {
            "total": getattr(result, "total", None),
            "offset": getattr(result, "offset", None),
            "limit": getattr(result, "limit", None),
            "has_more": getattr(result, "has_more", None),
            "items": list(result),
        }
    if isinstance(result, (dict, list)):
        return result
    return str(result)


def _needs_identifier(method_name: str, fn: Any) -> bool:
    """Return True if the method requires an identifier as first arg."""
    sig = inspect.signature(fn)
    params = [p for p in sig.parameters if p != "self"]
    if not params:
        return False
    first = params[0]
    # identifier or source (e.g. sources.statistics(source))
    return first in ("identifier", "source")


def main() -> int:
    try:
        from malloryapi import MalloryApi  # noqa: E402
    except ImportError:
        _write_error(
            "malloryapi is not installed. Run: pip install malloryapi"
        )
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
        nargs="?",
        default=None,
        help="Identifier (CVE ID, UUID) for get/export/sub-resource methods",
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
        "--urls",
        action="append",
        default=None,
        help="URLs for references create (repeat or comma-separated)",
    )

    args = parser.parse_args()

    if args.help_resources:
        client = MalloryApi(api_key=args.api_key or "help")
        out: dict[str, list[str]] = {}
        for attr in RESOURCE_NAMES:
            res = getattr(client, attr, None)
            if res is not None:
                out[attr] = _get_public_methods(res)
        aliases = [
            f"  {alias} -> {full}"
            for alias, full in sorted(RESOURCE_ALIASES.items())
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

    if args.resource is None:
        parser.print_help()
        sys.stderr.write(
            "\nUse malloryapi --help-resources to list resources and methods.\n"
        )
        return 0

    resolved = _resolve_resource_name(args.resource)
    client_kw: dict[str, Any] = {"api_key": args.api_key}
    if args.base_url is not None:
        client_kw["base_url"] = args.base_url
    try:
        client = MalloryApi(**client_kw)
    except Exception as e:
        _write_error(str(e))
        return 1

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

    kwargs: dict[str, Any] = {}
    if args.limit is not None:
        kwargs["limit"] = args.limit
    if args.offset is not None:
        kwargs["offset"] = args.offset
    if args.sort is not None:
        kwargs["sort"] = args.sort
    if args.order is not None:
        kwargs["order"] = args.order
    if args.filter_ is not None:
        kwargs["filter"] = args.filter_
    if args.period is not None:
        kwargs["period"] = args.period
    if args.q is not None:
        kwargs["q"] = args.q
    if args.types is not None:
        kwargs["types"] = args.types
    if args.urls is not None:
        urls: list[str] = []
        for u in args.urls:
            urls.extend(s.strip() for s in u.split(",") if s.strip())
        kwargs["urls"] = urls

    try:
        if _needs_identifier(args.method, method_fn):
            if not args.identifier:
                _write_error(
                    f"Method '{args.method}' requires an identifier"
                )
                return 1
            result = method_fn(args.identifier, **kwargs)
        else:
            if args.method == "query" and "q" not in kwargs:
                _write_error("Search query requires --q")
                return 1
            if args.method == "create" and "urls" not in kwargs:
                _write_error("references create requires --urls")
                return 1
            result = method_fn(**kwargs)
    except Exception as exc:
        from malloryapi.exceptions import APIError  # noqa: E402

        if isinstance(exc, APIError):
            _write_error(str(exc), getattr(exc, "status_code", None))
        else:
            _write_error(str(exc))
        return 1

    output = _serialize_result(result)
    if args.raw and isinstance(output, dict) and "items" in output:
        output = output.get("items", output)
    indent = None if args.compact else 2
    sys.stdout.write(json.dumps(output, indent=indent, default=str) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
