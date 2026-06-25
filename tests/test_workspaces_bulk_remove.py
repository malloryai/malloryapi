"""Tests for workspaces bulk-remove methods."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


WS = "ws-1"


class TestWorkspacesBulkRemove:
    def test_remove_entities(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_entities(WS, {"entities": ["e-1"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_entities" in str(request.url)

    def test_remove_sources(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_sources(WS, {"sources": ["s-1"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_sources" in str(request.url)

    def test_remove_topics(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_topics(WS, {"topics": ["ransomware"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_topics" in str(request.url)

    @pytest.mark.asyncio
    async def test_remove_entities_async(self, async_client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        await async_client.workspaces.remove_entities(WS, {"entities": ["e-1"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_entities" in str(request.url)

    @pytest.mark.asyncio
    async def test_remove_topics_async(self, async_client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        await async_client.workspaces.remove_topics(WS, {"topics": ["apt"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_topics" in str(request.url)
