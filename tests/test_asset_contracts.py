"""Focused contracts for asset matches and legacy inventory routes."""

from __future__ import annotations

import json

import pytest

from malloryapi._types import PaginatedResponse


async def test_asset_match_filters_keep_zero_omit_none_and_preserve_envelope(sdk):
    envelope = {
        "tenant_uuid": "tenant-1",
        "total_count": 1,
        "offset": 3,
        "limit": 7,
        "rows": [
            {
                "uuid": "match-1",
                "entity_type": "vulnerability",
                "entity_uuid": "vulnerability-1",
                "asset_count": 0,
            }
        ],
    }
    sdk.respond(json=envelope)

    result = await sdk.call(
        sdk.client.assets.list_matches,
        offset=3,
        limit=7,
        asset_count=0,
        entity_type__in="vulnerability,product",
        created_at__lt=None,
    )

    request = sdk.requests[-1]
    assert request.url.path == "/v1/assets/matches"
    assert dict(request.url.params) == {
        "sort": "asset_count",
        "order": "desc",
        "offset": "3",
        "limit": "7",
        "asset_count": "0",
        "entity_type__in": "vulnerability,product",
    }
    assert result == envelope


async def test_asset_query_escapes_every_path_segment_and_preserves_payload(sdk):
    query = {
        "columns": ["hostname", "ip_address"],
        "filters": [
            {"column": "hostname", "op": "eq", "value": "host-1"}
        ],
        "order_by": [{"column": "hostname", "direction": "asc"}],
        "page": 0,
        "page_size": 25,
        "include_schema": True,
        "drop_unfilterable_filters": False,
    }
    envelope = {
        "source_table": "plugin/table",
        "columns": [{"name": "hostname", "filterable": True}],
        "rows": [{"hostname": "host-1", "ip_address": "192.0.2.1"}],
        "page": 0,
        "page_size": 25,
        "total": 1,
        "total_is_capped": False,
        "has_more": False,
    }
    sdk.respond(json=envelope)

    result = await sdk.call(
        sdk.client.assets.query_matched_assets,
        "technology/product",
        "entity/one ?",
        "plugin/table",
        query,
    )

    request = sdk.requests[-1]
    assert request.method == "POST"
    assert request.url.raw_path.decode() == (
        "/v1/assets/matches/technology%2Fproduct/entity%2Fone%20%3F/"
        "assets/plugin%2Ftable/query"
    )
    assert json.loads(request.content) == query
    assert result == envelope


LEGACY_ASSET_ROUTES = [
    pytest.param(
        "inventory_hosts",
        (),
        {"limit": 10},
        "GET",
        "/v1/assets/inventory/hosts",
        {"items": [{"uuid": "host-1"}], "total": 1, "offset": 0, "limit": 10},
        True,
        id="inventory-hosts",
    ),
    pytest.param(
        "inventory_software",
        (),
        {},
        "GET",
        "/v1/assets/inventory/software",
        {"items": [{"uuid": "software-1"}], "total": 1},
        True,
        id="inventory-software",
    ),
    pytest.param(
        "vulnerabilities",
        (),
        {"status": "open"},
        "GET",
        "/v1/assets/vulnerabilities",
        {"items": [{"uuid": "instance-1", "status": "open"}], "total": 1},
        True,
        id="vulnerabilities",
    ),
    pytest.param(
        "profile",
        (),
        {},
        "GET",
        "/v1/assets/profile",
        {"hosts": 5, "software": 12},
        False,
        id="profile",
    ),
    pytest.param(
        "profile_for",
        ("host/type",),
        {},
        "GET",
        "/v1/assets/profile/host%2Ftype",
        {"entity_type": "host/type", "count": 3},
        False,
        id="profile-for",
    ),
    pytest.param(
        "exposure_check",
        ({"entities": ["192.0.2.1"], "entity_types": ["ip_address"]},),
        {},
        "POST",
        "/v1/assets/exposure-check",
        {"matches": []},
        False,
        id="exposure-check",
    ),
    pytest.param(
        "uploads",
        (),
        {"status": "complete"},
        "GET",
        "/v1/assets/uploads",
        {"items": [{"uuid": "upload-1", "status": "complete"}], "total": 1},
        True,
        id="uploads",
    ),
    pytest.param(
        "upload_status",
        ("upload/one",),
        {},
        "GET",
        "/v1/assets/uploads/upload%2Fone/status",
        {"uuid": "upload/one", "status": "complete"},
        False,
        id="upload-status",
    ),
    pytest.param(
        "upload_retry",
        ("upload/one",),
        {},
        "POST",
        "/v1/assets/uploads/upload%2Fone/retry",
        {"uuid": "upload/one", "status": "queued"},
        False,
        id="upload-retry",
    ),
]


@pytest.mark.parametrize(
    "method_name,args,kwargs,http_method,path,response,is_page",
    LEGACY_ASSET_ROUTES,
)
async def test_legacy_asset_routes_absent_from_openapi_remain_available(
    sdk,
    method_name,
    args,
    kwargs,
    http_method,
    path,
    response,
    is_page,
):
    sdk.respond(json=response)

    result = await sdk.call(
        getattr(sdk.client.assets, method_name), *args, **kwargs
    )

    request = sdk.requests[-1]
    assert request.method == http_method
    assert request.url.raw_path.decode().split("?", 1)[0] == path
    if is_page:
        assert isinstance(result, PaginatedResponse)
        assert result.items == response["items"]
    else:
        assert result == response
