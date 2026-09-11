"""Behavior contracts that endpoint discovery alone cannot prove."""

from __future__ import annotations

import json

import pytest

from malloryapi._types import PaginatedResponse


async def test_story_update_distinguishes_omitted_fields_from_explicit_null(sdk):
    sdk.respond(
        json={
            "uuid": "story-1",
            "title": "Incident update",
            "description": None,
        }
    )

    await sdk.call(sdk.client.stories.update, "story-1")
    sdk.respond(
        json={
            "uuid": "story-1",
            "title": "Incident update",
            "description": None,
        }
    )
    await sdk.call(
        sdk.client.stories.update,
        "story-1",
        description=None,
        reason="editorial correction",
    )

    empty_update, null_update = sdk.requests
    assert json.loads(empty_update.content) == {}
    assert not empty_update.url.params
    assert json.loads(null_update.content) == {"description": None}
    assert dict(null_update.url.params) == {"reason": "editorial correction"}


async def test_reference_submitter_distinguishes_omission_from_null(sdk):
    sdk.respond(json={"created": 1, "references": ["reference-1"]})

    await sdk.call(sdk.client.references.create, ["https://example.test/advisory"])
    sdk.respond(json={"created": 1, "references": ["reference-1"]})
    await sdk.call(
        sdk.client.references.create,
        ["https://example.test/advisory"],
        submitter=None,
    )

    omitted, explicit_null = sdk.requests
    assert json.loads(omitted.content) == {
        "urls": ["https://example.test/advisory"]
    }
    assert json.loads(explicit_null.content) == {
        "urls": ["https://example.test/advisory"],
        "submitter": None,
    }


async def test_story_observables_track_first_and_last_page(sdk):
    observables = [
        {
            "uuid": f"observable-{index}",
            "type": "domain",
            "name": f"host-{index}.example.test",
        }
        for index in range(10)
    ]
    sdk.respond(json={"observables": observables, "total": 30})

    first = await sdk.call(
        sdk.client.stories.observables, "story-1", offset=0, limit=10
    )
    sdk.respond(json={"observables": observables, "total": 30})
    last = await sdk.call(
        sdk.client.stories.observables, "story-1", offset=20, limit=10
    )

    assert first == PaginatedResponse(
        items=observables, total=30, offset=0, limit=10
    )
    assert first.has_more
    assert last == PaginatedResponse(
        items=observables, total=30, offset=20, limit=10
    )
    assert not last.has_more


async def test_observable_type_and_name_are_independently_escaped(sdk):
    page = {
        "data": [
            {
                "uuid": "entity-1",
                "entity_type": "vulnerability",
                "display_name": "CVE-2026-0001",
            }
        ],
        "total": 1,
        "offset": 2,
        "limit": 3,
    }
    sdk.respond(json=page)

    result = await sdk.call(
        sdk.client.observables.entities_by_type_name,
        "domain/type",
        "bad/name ?",
        entity_type="vulnerability",
        offset=2,
        limit=3,
    )

    request = sdk.requests[-1]
    assert request.url.raw_path.decode().split("?", 1)[0] == (
        "/v1/observables/domain%2Ftype/bad%2Fname%20%3F/entities"
    )
    assert result == PaginatedResponse(
        items=page["data"], total=1, offset=2, limit=3
    )


@pytest.mark.parametrize("period", ["7d", "30d"])
async def test_vulnerability_trending_derives_the_list_sort(period, sdk):
    sdk.respond(json={"data": [], "total": 0, "offset": 0, "limit": 100})

    await sdk.call(sdk.client.vulnerabilities.trending, period=period)

    assert sdk.requests[-1].url.params["sort"] == f"trending_{period}"


LEGACY_CONTENT_ROUTES = [
    pytest.param(
        "stories",
        "exposure",
        ("story/one",),
        {"offset": 0, "limit": 50},
        "GET",
        "/v1/stories/story%2Fone/exposure",
        {"items": [], "total": 0, "offset": 0, "limit": 50},
        True,
        id="story-exposure",
    ),
    pytest.param(
        "vulnerabilities",
        "enrich",
        ("CVE/2026-0001",),
        {},
        "POST",
        "/v1/vulnerabilities/CVE%2F2026-0001/enrich",
        {"status": "started", "uuid": "vulnerability-1"},
        False,
        id="vulnerability-enrich",
    ),
]


@pytest.mark.parametrize(
    "resource_name,method_name,args,kwargs,http_method,path,response,is_page",
    LEGACY_CONTENT_ROUTES,
)
async def test_legacy_content_routes_absent_from_openapi_remain_available(
    sdk,
    resource_name,
    method_name,
    args,
    kwargs,
    http_method,
    path,
    response,
    is_page,
):
    sdk.respond(json=response)

    resource = getattr(sdk.client, resource_name)
    result = await sdk.call(getattr(resource, method_name), *args, **kwargs)

    request = sdk.requests[-1]
    assert request.method == http_method
    assert request.url.raw_path.decode().split("?", 1)[0] == path
    if is_page:
        assert isinstance(result, PaginatedResponse)
        assert result.items == response["items"]
    else:
        assert result == response
