"""Regression tests for response-envelope contracts."""

from __future__ import annotations

import pytest

from malloryapi import InferenceResponse


async def test_paginated_response_preserves_envelope_metadata(sdk):
    sdk.respond(
        json={
            "data": [],
            "total": 0,
            "offset": 0,
            "limit": 50,
            "message": "No matching stories",
            "results_by_day": {},
            "results_by_month": {},
        }
    )

    response = await sdk.call(sdk.client.stories.list, limit=50)

    assert response.items == []
    assert response.total == 0
    assert response.metadata == {
        "message": "No matching stories",
        "results_by_day": {},
        "results_by_month": {},
    }


async def test_vtpcs_exposes_only_the_published_search_resource(sdk):
    assert not hasattr(sdk.client.vtpcs, "list")


INFERENCE_ENVELOPE = {
    "resolution": {
        "status": "resolved",
        "method": "canonical_name",
        "product": {
            "uuid": "11111111-1111-4111-8111-111111111111",
            "internal_name": "acme_widget",
            "name": "widget",
            "display_name": "Acme Widget",
            "organization": {
                "uuid": "22222222-2222-4222-8222-222222222222",
                "internal_name": "acme",
                "name": "acme",
                "display_name": "Acme",
            },
        },
        "candidates": [],
        "matched_aliases": [
            {
                "entity_type": "technology_product",
                "external_name": "Widget",
                "internal_name": "acme_widget",
            }
        ],
        "reason_codes": [],
        "candidates_truncated": False,
    },
    "normalized_request": {"vendor": "Acme", "product": "Widget", "part": "a"},
    "mode": "configuration_match",
    "coverage": {
        "basis": "mallory_normalized_configurations",
        "evaluation_complete": True,
        "configurations_examined": 1,
        "unknown_configurations": 0,
        "unknown_only_cves": 0,
        "unknown_only_cves_excluded": 0,
        "reason_codes": [],
    },
    "total": 1,
    "offset": 0,
    "limit": 50,
    "data": [
        {
            "vulnerability_uuid": "33333333-3333-4333-8333-333333333333",
            "cve_id": "CVE-2026-0001",
            "match_status": "matched",
            "reason_codes": [],
            "environment_evaluation": "not_evaluated",
            "evidence": [
                {
                    "configuration_uuid": "44444444-4444-4444-8444-444444444444"
                }
            ],
            "evidence_total": 1,
            "evidence_truncated": False,
        }
    ],
}


@pytest.mark.parametrize(
    ("resource_name", "expected_path"),
    [
        (
            "vulnerable_configurations",
            "/v1/vulnerable_technology_product_configuration_sets/search",
        ),
        ("vtpcs", "/v1/vtpcs/search"),
    ],
)
async def test_inference_search_preserves_decision_metadata(
    sdk, resource_name, expected_path
):
    sdk.respond(json=INFERENCE_ENVELOPE)
    resource = getattr(sdk.client, resource_name)

    result = await sdk.call(
        resource.search,
        {"vendor": "Acme", "product": "Widget", "part": "a"},
        offset=0,
        limit=25,
        include_unknown=False,
    )

    request = sdk.requests[-1]
    assert request.method == "POST"
    assert request.url.path == expected_path
    assert str(request.url.params) == "offset=0&limit=25&include_unknown=false"
    assert isinstance(result, InferenceResponse)
    assert result.items == INFERENCE_ENVELOPE["data"]
    assert result.resolution == INFERENCE_ENVELOPE["resolution"]
    assert result.normalized_request == INFERENCE_ENVELOPE["normalized_request"]
    assert result.mode == "configuration_match"
    assert result.coverage == INFERENCE_ENVELOPE["coverage"]


EXPORT = {
    "uuid": "55555555-5555-4555-8555-555555555555",
    "export_type": "stories",
    "export_strategy": "full",
    "version": "2026-09-11",
    "filepath": "exports/stories.json",
    "generated_at": "2026-09-11T12:00:00Z",
    "created_at": "2026-09-11T12:00:00Z",
    "updated_at": "2026-09-11T12:00:00Z",
}


@pytest.mark.parametrize("method_name", ["list", "history"])
async def test_exports_parse_complete_non_paginated_envelope(sdk, method_name):
    sdk.respond(json={"total_found": 240, "exports": [EXPORT]})

    result = await sdk.call(getattr(sdk.client.exports, method_name), limit=1)

    assert result.items == [EXPORT]
    assert result.total == 240
    assert result.limit == 240
    assert result.metadata == {"total_found": 240}
    assert result.has_more is False


async def test_geographies_parse_complete_non_paginated_envelope(sdk):
    countries = [
        {
            "code": f"C{index:03}",
            "name": f"Country {index}",
            "alpha_3": f"X{index:02}"[-3:],
            "numeric": f"{index:03}",
        }
        for index in range(249)
    ]
    sdk.respond(json={"countries": countries})

    result = await sdk.call(sdk.client.geographies.list)

    assert len(result) == 249
    assert result[0] == {
        "code": "C000",
        "name": "Country 0",
        "alpha_3": "X00",
        "numeric": "000",
    }
    assert result.total == 249
    assert result.limit == 249
    assert result.has_more is False
