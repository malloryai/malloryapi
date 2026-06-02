"""Tests for the packages resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


LIST_RESPONSE = {
    "items": [{"uuid": "p-1"}, {"uuid": "p-2"}],
    "total": 2,
    "offset": 0,
    "limit": 50,
}


class TestPackages:
    def test_list(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        result = client.packages.list(limit=10)
        request = httpx_mock.get_request()
        assert "/packages" in str(request.url)
        assert len(result) == 2

    def test_get(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": "p-1"})
        result = client.packages.get("p-1")
        request = httpx_mock.get_request()
        assert "/packages/p-1" in str(request.url)
        assert result["uuid"] == "p-1"

    def test_compromises(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.packages.compromises("p-1", compromise_type="typo")
        request = httpx_mock.get_request()
        assert "/packages/p-1/compromises" in str(request.url)
        assert "compromise_type=typo" in str(request.url)

    def test_configurations(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.packages.configurations("p-1")
        request = httpx_mock.get_request()
        assert "/packages/p-1/configurations" in str(request.url)

    def test_mentions(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.packages.mentions("p-1")
        request = httpx_mock.get_request()
        assert "/packages/p-1/mentions" in str(request.url)
