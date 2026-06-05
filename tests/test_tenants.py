"""Tests for the tenants resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


LIST_RESPONSE = {
    "items": [{"uuid": "t-1"}, {"uuid": "t-2"}],
    "total": 2,
    "offset": 0,
    "limit": 50,
}


class TestTenants:
    def test_list(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        result = client.tenants.list(limit=10)
        request = httpx_mock.get_request()
        assert "/tenants" in str(request.url)
        assert len(result) == 2

    def test_users(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": [{"uuid": "u-1"}]})
        result = client.tenants.users("t-1")
        request = httpx_mock.get_request()
        assert "/tenants/t-1/users" in str(request.url)
        assert len(result) == 1
