"""Tests for the extensions resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import AsyncMalloryApi, MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


LIST_RESPONSE = {
    "items": [{"uuid": "ext-1"}, {"uuid": "ext-2"}],
    "total": 2,
    "offset": 0,
    "limit": 50,
}


class TestExtensions:
    def test_registered_on_client(self, client):
        assert hasattr(client, "extensions")

    def test_list(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        result = client.extensions.list(limit=10)
        request = httpx_mock.get_request()
        assert "/extensions" in str(request.url)
        assert len(result) == 2

    def test_list_forwards_filter_kwargs(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        client.extensions.list(marketplace="vscode", publisher__ilike="micro%")
        request = httpx_mock.get_request()
        assert request.url.params["marketplace"] == "vscode"
        assert request.url.params["publisher__ilike"] == "micro%"

    def test_get(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": "ext-1"})
        result = client.extensions.get("ext-1")
        request = httpx_mock.get_request()
        assert "/extensions/ext-1" in str(request.url)
        assert result["uuid"] == "ext-1"

    def test_configurations(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.extensions.configurations("ext-1")
        request = httpx_mock.get_request()
        assert "/extensions/ext-1/configurations" in str(request.url)

    def test_mentions(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.extensions.mentions("ext-1")
        request = httpx_mock.get_request()
        assert "/extensions/ext-1/mentions" in str(request.url)


class TestAsyncExtensions:
    async def test_registered_on_client(self):
        c = AsyncMalloryApi(api_key="test-key")
        assert hasattr(c, "extensions")
        await c.aclose()

    async def test_list(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        c = AsyncMalloryApi(api_key="test-key")
        result = await c.extensions.list(limit=10)
        request = httpx_mock.get_request()
        assert "/extensions" in str(request.url)
        assert len(result) == 2
        await c.aclose()

    async def test_configurations(self, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        c = AsyncMalloryApi(api_key="test-key")
        await c.extensions.configurations("ext-1")
        request = httpx_mock.get_request()
        assert "/extensions/ext-1/configurations" in str(request.url)
        await c.aclose()
