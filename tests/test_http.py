"""Tests for the SDK's shared HTTP transport behavior."""

import json

import pytest

from malloryapi.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


@pytest.mark.parametrize("payload", [None, 0, False, [], [0, False, None]])
async def test_success_responses_preserve_any_json_value(sdk, payload):
    sdk.respond(json=payload)

    result = await sdk.call(sdk.client.health)

    assert json.dumps(result) == json.dumps(payload)


async def test_no_content_response_returns_none(sdk):
    sdk.respond(status_code=204)

    assert await sdk.call(sdk.client.workspaces.delete, "workspace-1") is None


async def test_query_parameters_omit_only_none(sdk):
    sdk.respond(json={"data": [], "total": 0, "offset": 0, "limit": 100})

    await sdk.call(
        sdk.client.stories.list,
        offset=0,
        include_proto=False,
        workspace_uuids=["workspace-1", "workspace-2"],
        created_at__gte=None,
    )

    params = sdk.requests[-1].url.params
    assert "created_at__gte" not in params
    assert params["offset"] == "0"
    assert params["include_proto"] == "false"
    assert params.get_list("workspace_uuids") == ["workspace-1", "workspace-2"]


async def test_patch_forwards_body_and_query_parameters(sdk):
    sdk.respond(json={"uuid": "story-1", "title": "Updated"})

    await sdk.call(
        sdk.client.stories.update,
        "story-1",
        title="Updated",
        reason="editorial correction",
    )

    request = sdk.requests[-1]
    assert request.method == "PATCH"
    assert request.url.path == "/v1/stories/story-1"
    assert dict(request.url.params) == {"reason": "editorial correction"}
    assert request.read() == b'{"title":"Updated"}'


@pytest.mark.parametrize(
    ("status_code", "body", "error_type"),
    [
        (401, {"detail": "Invalid authentication credentials"}, AuthenticationError),
        (403, {"detail": "Forbidden"}, AuthenticationError),
        (404, {"detail": "Not found"}, NotFoundError),
        (
            422,
            {
                "detail": [
                    {
                        "type": "greater_than_equal",
                        "loc": ["query", "offset"],
                        "msg": "Input should be greater than or equal to 0",
                        "input": "-1",
                        "ctx": {"ge": 0},
                    }
                ]
            },
            ValidationError,
        ),
        (429, {"detail": "Too many requests"}, RateLimitError),
    ],
)
async def test_json_errors_preserve_status_and_body(
    sdk, status_code, body, error_type
):
    sdk.respond(json=body, status_code=status_code)

    with pytest.raises(error_type) as raised:
        await sdk.call(sdk.client.health)

    assert raised.value.status_code == status_code
    assert raised.value.response_body == body


async def test_non_json_error_preserves_response_text(sdk):
    sdk.respond(
        content="upstream unavailable",
        status_code=500,
        headers={"content-type": "text/plain"},
    )

    with pytest.raises(APIError) as raised:
        await sdk.call(sdk.client.health)

    assert raised.value.status_code == 500
    assert raised.value.response_body == "upstream unavailable"


async def test_closing_sdk_closes_its_http_client(sdk):
    close = getattr(sdk.client, "aclose", None) or sdk.client.close
    await sdk.call(close)

    with pytest.raises(RuntimeError, match="client has been closed"):
        await sdk.call(sdk.client.health)
