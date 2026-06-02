"""Tests for breaches export method."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


class TestBreachesExport:
    def test_export(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"export": "data"})
        result = client.breaches.export("b-1")
        request = httpx_mock.get_request()
        assert "/breaches/b-1/export" in str(request.url)
        assert result == {"export": "data"}

    def test_export_with_params(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"export": "data"})
        client.breaches.export(
            "b-1",
            relationships_created_after="2024-01-01",
            relationships_created_before="2024-12-31",
        )
        request = httpx_mock.get_request()
        url = str(request.url)
        assert "/breaches/b-1/export" in url
        assert "relationships_created_after=2024-01-01" in url
        assert "relationships_created_before=2024-12-31" in url
