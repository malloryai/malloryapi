"""Tests for the geographies resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


class TestGeographies:
    def test_list(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=[{"code": "US"}, {"code": "GB"}])
        result = client.geographies.list()
        request = httpx_mock.get_request()
        assert "/geographies" in str(request.url)
        assert result[0]["code"] == "US"

    def test_get(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"code": "US", "name": "United States"})
        result = client.geographies.get("US")
        request = httpx_mock.get_request()
        assert "/geographies/US" in str(request.url)
        assert result["code"] == "US"
