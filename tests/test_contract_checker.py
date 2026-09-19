"""Fault injection proves the offline checker detects broken SDK contracts."""

from __future__ import annotations

from urllib.parse import quote

import httpx
import pytest

from scripts.check_openapi import check_client


@pytest.fixture
def spec():
    return {
        "paths": {
            "/v1/widgets": {
                "get": {
                    "parameters": [
                        {
                            "name": "offset",
                            "in": "query",
                            "schema": {
                                "type": "integer",
                                "minimum": 0,
                                "default": 7,
                            },
                        },
                        {
                            "name": "enabled",
                            "in": "query",
                            "schema": {
                                "type": "boolean",
                                "default": False,
                            },
                        },
                        {
                            "name": "tags",
                            "in": "query",
                            "schema": {
                                "anyOf": [
                                    {"type": "array", "items": {"type": "string"}},
                                    {"type": "null"},
                                ],
                            },
                        },
                    ],
                },
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "label": {
                                            "anyOf": [
                                                {"type": "string"},
                                                {"type": "null"},
                                            ]
                                        },
                                        "options": {
                                            "type": "object",
                                            "properties": {
                                                "enabled": {"type": "boolean"},
                                                "count": {"type": "integer"},
                                                "tags": {
                                                    "type": "array",
                                                    "items": {"type": "string"},
                                                },
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    },
                },
            },
            "/v1/widgets/{uuid}": {
                "get": {
                    "parameters": [
                        {"name": "uuid", "in": "path", "schema": {"type": "string"}},
                    ]
                },
            },
        },
    }


def toy_client(fault=None):
    """A tiny SDK with independently specified routes and injectable defects."""

    class Widgets:
        def __init__(self, http):
            self._http = http

        def list(self, **params):
            path = "/v1/widgets"
            if fault == "query_route" and params:
                path = "/v1/wrong"
            params = {key: value for key, value in params.items() if value is not None}
            if fault == "query":
                params.pop("offset", None)
            if fault == "boolean" and params.get("enabled") is False:
                params.pop("enabled")
            return self._http.get(path, params=params).json()

        def get(self, identifier):
            if fault == "missing":
                return None
            encoded = identifier if fault == "escaping" else quote(identifier, safe="")
            path = "/v1/wrong" if fault == "route" else f"/v1/widgets/{encoded}"
            if fault == "duplicate":
                self._http.get(path)
            return self._http.get(path).json()

        def create(self, data: dict):
            payload = dict(data)
            if fault == "extra":
                payload["unexpected"] = True
            if fault == "body":
                payload.pop("label", None)
            if fault == "null" and payload.get("label") is None:
                payload.pop("label", None)
            if fault == "body_boolean" and "options" in payload:
                payload["options"] = {**payload["options"], "enabled": 1}
            if fault == "nested" and "options" in payload:
                payload["options"] = {"enabled": True}
            return self._http.post("/v1/widgets", json=payload).json()

    class Client:
        def __init__(self, *, api_key, transport):
            self._http = httpx.Client(
                base_url="https://example.test", transport=transport
            )
            self.widgets = Widgets(self._http)

        def close(self):
            self._http.close()

    return Client


async def test_checker_accepts_complete_transport_contract(spec):
    result = await check_client(spec, toy_client())
    assert result == {
        "client": "Client",
        "operations": 3,
        "query_parameters": 3,
        "path_parameters": 1,
        "header_parameters": 0,
        "body_contracts": 1,
        "issues": [],
    }


@pytest.mark.parametrize(
    ("fault", "issue"),
    [
        ("missing", "Missing operation: GET /v1/widgets/{uuid}"),
        ("duplicate", "expected one request, got 2"),
        ("route", "Missing operation: GET /v1/widgets/{uuid}"),
        ("escaping", "path parameter uuid"),
        ("query", "query offset="),
        ("query_route", "route"),
        ("boolean", "query enabled=False"),
        ("body", "JSON field label"),
        ("null", "JSON field label"),
        ("nested", "JSON field options"),
        ("body_boolean", "JSON field options"),
    ],
)
async def test_checker_rejects_injected_faults(spec, fault, issue):
    result = await check_client(spec, toy_client(fault))
    assert any(issue in message for message in result["issues"]), result


@pytest.mark.parametrize("fault", [None, "extra"])
async def test_checker_preserves_arbitrary_json_body(spec, fault):
    spec["paths"]["/v1/widgets"]["post"]["requestBody"]["content"]["application/json"][
        "schema"
    ] = {"type": "object"}
    result = await check_client(spec, toy_client(fault))
    if fault is None:
        assert result["issues"] == []
    else:
        assert any("arbitrary JSON body" in issue for issue in result["issues"])


@pytest.mark.parametrize("drop_header", [False, True])
async def test_checker_validates_header_parameters(drop_header):
    class Client:
        def __init__(self, *, api_key, transport):
            self._http = httpx.Client(
                base_url="https://example.test", transport=transport
            )

        def create(self, *, idempotency_key: str):
            headers = {} if drop_header else {"Idempotency-Key": idempotency_key}
            return self._http.post("/v1/samples", headers=headers).json()

        def close(self):
            self._http.close()

    spec = {
        "paths": {
            "/v1/samples": {
                "post": {
                    "parameters": [
                        {
                            "name": "Idempotency-Key",
                            "in": "header",
                            "schema": {"type": "string"},
                        }
                    ]
                }
            }
        }
    }
    result = await check_client(spec, Client)
    if drop_header:
        assert any("header Idempotency-Key" in issue for issue in result["issues"])
    else:
        assert result["issues"] == []
