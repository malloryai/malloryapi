"""Tests for added stories methods."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


class TestStoriesMethods:
    def test_exposure(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            json={"items": [], "total": 0, "offset": 0, "limit": 50}
        )
        client.stories.exposure("story-1", offset=0, limit=50)
        request = httpx_mock.get_request()
        assert "/stories/story-1/exposure" in str(request.url)

    def test_topics_taxonomy(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"taxonomy": []})
        result = client.stories.topics_taxonomy()
        request = httpx_mock.get_request()
        assert "/stories/topics/taxonomy" in str(request.url)
        assert result == {"taxonomy": []}
