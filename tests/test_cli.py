"""Tests for the malloryapi CLI."""

from __future__ import annotations

import json
import os
from io import StringIO
from unittest.mock import patch

import pytest
from pytest_httpx import HTTPXMock

from malloryapi.cli import main

TEST_API_KEY = "test-api-key-1234"


def _run_cli(argv: list[str], env: dict | None = None) -> tuple[int, str, str]:
    """Run CLI with argv; return (exit_code, stdout, stderr)."""
    env = env or {}
    with patch("sys.argv", ["malloryapi"] + argv), patch(
        "sys.stdout", StringIO()
    ), patch("sys.stderr", StringIO()) as stderr, patch(
        "sys.stdin", StringIO()
    ):
        out = StringIO()
        err = StringIO()
        with patch("sys.stdout", out), patch("sys.stderr", err):
            if env:
                with patch.dict(os.environ, env, clear=False):
                    code = main()
            else:
                code = main()
        return code, out.getvalue(), err.getvalue()


class TestCliHelpResources:
    def test_help_resources_exits_zero(self):
        code, out, err = _run_cli(
            ["--help-resources"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 0
        assert err == ""

    def test_help_resources_output_has_resources_and_aliases(self):
        code, out, err = _run_cli(
            ["--help-resources"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        data = json.loads(out)
        assert "resources" in data
        assert "aliases" in data
        assert "vulnerabilities" in data["resources"]
        assert "list" in data["resources"]["vulnerabilities"]
        assert "get" in data["resources"]["vulnerabilities"]
        assert data["aliases"]["vulns"] == "vulnerabilities"
        assert data["aliases"]["actors"] == "threat_actors"


class TestCliErrors:
    def test_unknown_resource_returns_one_and_lists_available(self):
        code, out, err = _run_cli(
            ["nonexistent", "list"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 1
        err_data = json.loads(err)
        assert "error" in err_data
        assert "Unknown resource" in err_data["error"]
        assert "nonexistent" in err_data["error"]

    def test_unknown_method_returns_one_and_lists_methods(self):
        code, out, err = _run_cli(
            ["vulnerabilities", "nonexistent"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 1
        err_data = json.loads(err)
        assert "error" in err_data
        assert "Unknown method" in err_data["error"]
        assert "list" in err_data["error"] or "get" in err_data["error"]

    def test_missing_method_returns_one(self):
        code, out, err = _run_cli(
            ["vulnerabilities"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 1
        err_data = json.loads(err)
        assert "Method required" in err_data["error"]

    def test_get_without_identifier_returns_one(self):
        code, out, err = _run_cli(
            ["vulnerabilities", "get"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 1
        err_data = json.loads(err)
        assert "requires an identifier" in err_data["error"]

    def test_search_query_without_q_returns_one(self):
        code, out, err = _run_cli(
            ["search", "query"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 1
        err_data = json.loads(err)
        assert "requires --q" in err_data["error"]


class TestCliDispatchAndOutput:
    def test_vulnerabilities_list_returns_paginated_json(
        self, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            json={
                "items": [
                    {"uuid": "a", "cve_id": "CVE-2024-0001"},
                ],
                "total": 1,
                "offset": 0,
                "limit": 10,
            }
        )
        code, out, err = _run_cli(
            ["vulnerabilities", "list", "--limit", "10"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 0
        assert err == ""
        data = json.loads(out)
        assert data["total"] == 1
        assert data["limit"] == 10
        assert len(data["items"]) == 1
        assert data["items"][0]["cve_id"] == "CVE-2024-0001"

    def test_vulnerabilities_get_returns_detail_json(
        self, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            json={
                "uuid": "abc",
                "cve_id": "CVE-2024-1234",
                "cvss_base_score": 9.8,
            }
        )
        code, out, err = _run_cli(
            ["vulnerabilities", "get", "CVE-2024-1234"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 0
        assert err == ""
        data = json.loads(out)
        assert data["cve_id"] == "CVE-2024-1234"
        assert data["cvss_base_score"] == 9.8

    def test_alias_vulns_resolves_to_vulnerabilities(
        self, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 5}
        )
        code, out, err = _run_cli(
            ["vulns", "list", "--limit", "5"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 0
        request = httpx_mock.get_request()
        assert "/vulnerabilities" in str(request.url)

    def test_compact_output_single_line(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 10}
        )
        code, out, err = _run_cli(
            ["vulnerabilities", "list", "--limit", "10", "--compact"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 0
        assert "\n" not in out.strip() or out.strip().count("\n") == 0
        data = json.loads(out)
        assert "items" in data

    def test_api_error_writes_json_to_stderr(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(status_code=404, json={"detail": "Not found"})
        code, out, err = _run_cli(
            ["vulnerabilities", "get", "CVE-9999-9999"],
            env={"MALLORY_API_KEY": TEST_API_KEY},
        )
        assert code == 1
        err_data = json.loads(err)
        assert "error" in err_data
        assert err_data.get("status_code") == 404
