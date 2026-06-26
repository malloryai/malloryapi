"""Tests for added workspaces methods."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


WS = "ws-1"


class TestWorkspacesMethods:
    def test_add_sources(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.add_sources(WS, {"sources": ["s-1"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/add_sources" in str(request.url)

    def test_members(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=[{"user_uuid": "u-1"}])
        result = client.workspaces.members(WS)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/workspaces/ws-1/members" in str(request.url)
        assert result == [{"user_uuid": "u-1"}]

    def test_add_member(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.add_member(
            WS, {"user_uuid": "u-1", "role": "admin"}
        )
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/members" in str(request.url)

    def test_update_member(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.update_member(WS, "u-1", {"role": "viewer"})
        request = httpx_mock.get_request()
        assert request.method == "PATCH"
        assert "/workspaces/ws-1/members/u-1" in str(request.url)

    def test_remove_member(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_member(WS, "u-1")
        request = httpx_mock.get_request()
        assert request.method == "DELETE"
        assert "/workspaces/ws-1/members/u-1" in str(request.url)

    def test_sources(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 50}
        )
        client.workspaces.sources(WS, offset=0, limit=50)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/workspaces/ws-1/sources" in str(request.url)

    def test_remove_source(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_source(WS, "src-1")
        request = httpx_mock.get_request()
        assert request.method == "DELETE"
        assert "/workspaces/ws-1/sources/src-1" in str(request.url)

    def test_remove_entity(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_entity(WS, "malware", "e-1")
        request = httpx_mock.get_request()
        assert request.method == "DELETE"
        assert "/workspaces/ws-1/entities/malware/e-1" in str(request.url)

    def test_remove_topic(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_topic(WS, "ransomware")
        request = httpx_mock.get_request()
        assert request.method == "DELETE"
        assert "/workspaces/ws-1/topics/ransomware" in str(request.url)

    def test_remove_entities(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_entities(WS, {"entities": ["e-1"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_entities" in str(request.url)

    def test_remove_topics(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_topics(WS, {"topics": ["ransomware"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_topics" in str(request.url)

    def test_remove_sources(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        client.workspaces.remove_sources(WS, {"sources": ["s-1"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/workspaces/ws-1/remove_sources" in str(request.url)
