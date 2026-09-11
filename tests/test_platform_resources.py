"""Behavior regressions for findings and sightings."""

from __future__ import annotations

import json

from malloryapi._types import PaginatedResponse


async def test_finding_list_defaults_and_page_metadata_survive_the_round_trip(sdk):
    sdk.respond(
        json={
            "data": [
                {
                    "uuid": "finding-1",
                    "definition_slug": "public-port",
                    "title": "Public management port",
                    "severity": "high",
                    "status": "open",
                }
            ],
            "total": 8,
            "offset": 0,
            "limit": 50,
            "results_by_day": {"2026-09-11": 1},
        }
    )

    result = await sdk.call(sdk.client.findings.list)

    assert isinstance(result, PaginatedResponse)
    assert result.items[0]["definition_slug"] == "public-port"
    assert result.total == 8
    assert result.metadata == {"results_by_day": {"2026-09-11": 1}}
    assert dict(sdk.requests[-1].url.params) == {
        "sort": "updated_at",
        "order": "desc",
        "offset": "0",
        "limit": "50",
    }


async def test_finding_ticket_path_escapes_each_identifier(sdk):
    sdk.respond(status_code=204)

    result = await sdk.call(
        sdk.client.findings.detach_finding,
        "ticket/one ?",
        "finding/two ?",
    )

    request = sdk.requests[-1]
    assert request.method == "DELETE"
    assert request.url.raw_path.decode() == (
        "/v1/findings/tickets/ticket%2Fone%20%3F/"
        "findings/finding%2Ftwo%20%3F"
    )
    assert result is None


async def test_sighting_bulk_preserves_nested_payload_and_result_envelope(sdk):
    payload = {
        "items": [
            {
                "observable_type": "domain",
                "observable_name": "example.test",
                "source": "sensor-1",
                "external_id": "event-1",
                "matched_at": "2026-09-11T12:34:56Z",
            }
        ]
    }
    envelope = {
        "created": 1,
        "existing": 0,
        "results": [
            {
                "status": "created",
                "sighting": {
                    "uuid": "sighting-1",
                    "tenant_uuid": "tenant-1",
                    "observable_uuid": "observable-1",
                    "observable_type": "domain",
                    "observable_name": "example.test",
                    "source": "sensor-1",
                    "external_id": "event-1",
                    "matched_at": "2026-09-11T12:34:56Z",
                    "created_at": "2026-09-11T12:35:00Z",
                },
                "index": 0,
            }
        ],
    }
    sdk.respond(json=envelope)

    result = await sdk.call(sdk.client.sightings.bulk, payload)

    request = sdk.requests[-1]
    assert request.method == "POST"
    assert request.url.path == "/v1/sightings/bulk"
    assert json.loads(request.content) == payload
    assert result == envelope
