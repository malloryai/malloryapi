"""Tests for the extensions resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi.resources.extensions import AsyncExtensions, Extensions


@pytest.fixture
def extensions(client):
    return Extensions(client._http)


@pytest.fixture
def async_extensions(async_client):
    return AsyncExtensions(async_client._http)


EXT = "ext-1"


class TestExtensions:
    def test_list(self, extensions, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 100}
        )
        extensions.list()
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/extensions" in str(request.url)

    def test_get(self, extensions, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": EXT})
        result = extensions.get(EXT)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/extensions/ext-1" in str(request.url)
        assert result == {"uuid": EXT}

    def test_configurations(self, extensions, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        extensions.configurations(EXT)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/extensions/ext-1/configurations" in str(request.url)

    def test_mentions(self, extensions, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        extensions.mentions(EXT)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/extensions/ext-1/mentions" in str(request.url)


class TestAsyncExtensions:
    @pytest.mark.asyncio
    async def test_list(self, async_extensions, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 100}
        )
        await async_extensions.list()
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/extensions" in str(request.url)

    @pytest.mark.asyncio
    async def test_get(self, async_extensions, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": EXT})
        result = await async_extensions.get(EXT)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/extensions/ext-1" in str(request.url)
        assert result == {"uuid": EXT}
