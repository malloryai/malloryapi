"""CLI behavior through the real SDK and an explicitly injected HTTP transport."""

import json

import httpx
import pytest

from malloryapi.cli import main


@pytest.fixture
def run_cli(capsys):
    def run(args, *, payload=None, status=200):
        requests = []

        def respond(request):
            assert not requests, "CLI dispatch must issue only one request"
            requests.append(request)
            return (
                httpx.Response(status, json=payload)
                if status != 204
                else httpx.Response(204)
            )

        class Transport(httpx.MockTransport):
            closed = False

            def close(self):
                self.closed = True
                super().close()

        transport = Transport(respond)
        code = main(["--api-key", "test-key", *args], transport=transport)
        output = capsys.readouterr()
        assert transport.closed, "CLI must close its client on success and failure"
        return code, output.out, output.err, requests

    return run


def test_discovery_includes_all_sdk_resources_and_aliases(run_cli):
    code, out, err, requests = run_cli(["--help-resources"])
    assert (code, err, requests) == (0, "", [])
    data = json.loads(out)
    assert data["aliases"]["vulns"] == "vulnerabilities"
    assert data["aliases"]["actors"] == "threat_actors"
    for resource in (
        "findings",
        "finding_definitions",
        "profiles",
        "sightings",
        "vtpcs",
        "extensions",
    ):
        assert resource in data["resources"]
    assert {"get", "list"} <= set(data["resources"]["vulnerabilities"])


@pytest.mark.parametrize(
    "args, error",
    [
        (["unknown", "list"], "Unknown resource"),
        (["vulnerabilities", "unknown"], "Unknown method"),
        (["vulnerabilities"], "Method required"),
        (["vulnerabilities", "get"], "requires an identifier"),
        (["search", "query"], "requires --q"),
        (["workspaces", "remove_member", "ws-1"], "user_uuid"),
        (["workspaces", "add_member", "ws-1", "not-json"], "must be valid JSON"),
        (["stories", "list", "--param", "broken"], "NAME=VALUE"),
        (["stories", "list", "--limit", "5", "--param", "limit=7"], "more than once"),
    ],
)
def test_invalid_invocations_report_error_without_http(args, error, run_cli):
    code, out, err, requests = run_cli(args)
    assert code == 1
    assert (out, requests) == ("", [])
    assert error in json.loads(err)["error"]


@pytest.mark.parametrize(
    "args, verb, path, body",
    [
        (["geo", "get", "US"], "GET", "/v1/geographies/US", None),
        (["tenants", "users", "t-1"], "GET", "/v1/tenants/t-1/users", None),
        (["assets", "profile_for", "host"], "GET", "/v1/assets/profile/host", None),
        (["geo", "list"], "GET", "/v1/geographies", None),
        (
            ["workspaces", "remove_member", "ws-1", "user-1"],
            "DELETE",
            "/v1/workspaces/ws-1/members/user-1",
            None,
        ),
        (
            ["workspaces", "remove_entity", "ws-1", "actor", "e-1"],
            "DELETE",
            "/v1/workspaces/ws-1/entities/actor/e-1",
            None,
        ),
        (
            ["workspaces", "add_member", "ws-1", '{"user_uuid":"u-1","role":"admin"}'],
            "POST",
            "/v1/workspaces/ws-1/members",
            {"user_uuid": "u-1", "role": "admin"},
        ),
        (
            ["findings", "update", '{"status":"closed"}', "--param", "uuid=f-1"],
            "PATCH",
            "/v1/findings/f-1",
            {"status": "closed"},
        ),
        (
            ["products", "search", '{"vendor":"acme","product":"widget"}'],
            "POST",
            "/v1/products/search",
            {"vendor": "acme", "product": "widget"},
        ),
    ],
)
def test_identifier_and_json_arguments_reach_the_correct_endpoint(
    args, verb, path, body, run_cli
):
    code, _, err, requests = run_cli(args, payload={"data": [], "total": 0})
    assert (code, err) == (0, "")
    assert len(requests) == 1
    assert (requests[0].method, requests[0].url.path) == (verb, path)
    assert (json.loads(requests[0].content) if requests[0].content else None) == body


def test_alias_and_typed_filters_preserve_values(run_cli):
    code, out, err, requests = run_cli(
        [
            "vulns",
            "list",
            "--param",
            "offset=0",
            "--param",
            "include_merged=false",
            "--param",
            "limit=7",
            "--base-url",
            "https://custom.example/v1",
        ],
        payload={
            "data": [{"cve_id": "CVE-2026-0001"}],
            "total": 1,
            "offset": 0,
            "limit": 7,
        },
    )
    assert (code, err) == (0, "")
    request = requests[0]
    assert request.url.host == "custom.example"
    assert request.url.path == "/v1/vulnerabilities"
    assert dict(request.url.params) == {
        "offset": "0",
        "limit": "7",
        "include_merged": "false",
    }
    assert json.loads(out)["items"] == [{"cve_id": "CVE-2026-0001"}]


@pytest.mark.parametrize(
    "flags, expected",
    [
        (["--raw"], [{"uuid": "one"}]),
        (
            ["--compact"],
            {
                "items": [{"uuid": "one"}],
                "total": 1,
                "offset": 0,
                "limit": 10,
                "metadata": {},
                "has_more": False,
            },
        ),
    ],
)
def test_output_modes(flags, expected, run_cli):
    code, out, err, _ = run_cli(
        ["stories", "list", *flags],
        payload={"data": [{"uuid": "one"}], "total": 1, "offset": 0, "limit": 10},
    )
    assert (code, err) == (0, "")
    assert json.loads(out) == expected
    if "--compact" in flags:
        assert out.count("\n") == 1


def test_inference_output_preserves_decision_metadata(run_cli):
    payload = {
        "data": [],
        "total": 0,
        "offset": 0,
        "limit": 50,
        "resolution": {"status": "unresolved"},
        "normalized_request": None,
        "mode": "configuration_match",
        "coverage": {"evaluation_complete": False},
    }
    code, out, err, _ = run_cli(
        ["vtpcs", "search", '{"vendor":"acme","product":"widget"}'], payload=payload
    )
    assert (code, err) == (0, "")
    result = json.loads(out)
    for key in ("resolution", "normalized_request", "mode", "coverage"):
        assert result[key] == payload[key]


def test_no_content_outputs_json_null(run_cli):
    code, out, err, requests = run_cli(["workspaces", "delete", "ws-1"], status=204)
    assert (code, err, json.loads(out)) == (0, "", None)
    assert len(requests) == 1


def test_api_errors_go_only_to_stderr(run_cli):
    code, out, err, _ = run_cli(
        ["vulnerabilities", "get", "missing"],
        status=404,
        payload={"detail": "Not found"},
    )
    assert (code, out) == (1, "")
    assert json.loads(err)["status_code"] == 404
