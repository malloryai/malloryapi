"""Tests for the profiles resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi.resources.profiles import AsyncProfiles, Profiles

PID = "p-1"


@pytest.fixture
def profiles(client):
    return Profiles(client._http)


@pytest.fixture
def async_profiles(async_client):
    return AsyncProfiles(async_client._http)


class TestProfiles:
    def test_list(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 100}
        )
        profiles.list(filter="name:test", sort="created_at", order="desc")
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/profiles" in str(request.url)

    def test_create(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": PID})
        profiles.create({"name": "test"})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert str(request.url).endswith("/profiles")

    def test_get(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": PID})
        profiles.get(PID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/profiles/p-1" in str(request.url)

    def test_update(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": PID})
        profiles.update(PID, {"name": "renamed"})
        request = httpx_mock.get_request()
        assert request.method == "PUT"
        assert "/profiles/p-1" in str(request.url)

    def test_delete(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        profiles.delete(PID)
        request = httpx_mock.get_request()
        assert request.method == "DELETE"
        assert "/profiles/p-1" in str(request.url)

    def test_add_entities(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        profiles.add_entities(PID, {"entities": ["e-1"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/profiles/p-1/add_entities" in str(request.url)

    def test_add_topics(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        profiles.add_topics(PID, {"topics": ["ransomware"]})
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/profiles/p-1/add_topics" in str(request.url)

    def test_entities(self, profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 100}
        )
        profiles.entities(PID, offset=0, limit=100)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/profiles/p-1/entities" in str(request.url)


class TestAsyncProfiles:
    @pytest.mark.asyncio
    async def test_list(self, async_profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 100}
        )
        await async_profiles.list()
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/profiles" in str(request.url)

    @pytest.mark.asyncio
    async def test_update(self, async_profiles, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"uuid": PID})
        await async_profiles.update(PID, {"name": "renamed"})
        request = httpx_mock.get_request()
        assert request.method == "PUT"
        assert "/profiles/p-1" in str(request.url)
