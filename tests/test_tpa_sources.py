"""Tests for technology product advisories sources method."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


class TestTpaSources:
    def test_sources(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=[{"name": "vendor-x"}])
        result = client.advisories.sources()
        request = httpx_mock.get_request()
        assert "/technology_product_advisories/sources" in str(request.url)
        assert result == [{"name": "vendor-x"}]
