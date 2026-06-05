"""Tests for threat actor geography/industry sub-resources."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


PAGINATED = {"items": [{"uuid": "g-1"}], "total": 1, "offset": 0, "limit": 50}


class TestActorGeographies:
    def test_source_geographies(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=PAGINATED)
        result = client.threat_actors.source_geographies("abc-123")
        request = httpx_mock.get_request()
        assert "/actors/abc-123/source-geographies" in str(request.url)
        assert len(result) == 1

    def test_target_geographies(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=PAGINATED)
        client.threat_actors.target_geographies("abc-123", type="country")
        request = httpx_mock.get_request()
        assert "/actors/abc-123/target-geographies" in str(request.url)
        assert "type=country" in str(request.url)

    def test_target_industries(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=PAGINATED)
        client.threat_actors.target_industries("abc-123", offset=0, limit=10)
        request = httpx_mock.get_request()
        assert "/actors/abc-123/target-industries" in str(request.url)
        assert "limit=10" in str(request.url)
