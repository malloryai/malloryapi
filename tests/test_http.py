"""Tests for the HTTP client layer."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi._http import SyncHttpClient
from malloryapi.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


@pytest.fixture
def http_client():
    client = SyncHttpClient(api_key="test-key")
    yield client
    client.close()


class TestSyncHttpClient:
    def test_auth_header(self, http_client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"ok": True})
        http_client.get("/test")
        request = httpx_mock.get_request()
        assert request.headers["authorization"] == "Bearer test-key"

    def test_get_success(self, http_client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": [], "total": 0})
        result = http_client.get("/vulnerabilities")
        assert result == {"items": [], "total": 0}

    def test_get_with_params(
        self, http_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(json={"items": []})
        http_client.get(
            "/vulnerabilities", params={"limit": 10}
        )
        request = httpx_mock.get_request()
        assert "limit=10" in str(request.url)

    def test_post_success(
        self, http_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(json={"id": "123"})
        result = http_client.post(
            "/references", json={"urls": ["https://example.com"]}
        )
        assert result == {"id": "123"}

    def test_401_raises_auth_error(
        self, http_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            status_code=401, json={"detail": "Unauthorized"}
        )
        with pytest.raises(AuthenticationError):
            http_client.get("/test")

    def test_403_raises_auth_error(
        self, http_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            status_code=403, json={"detail": "Forbidden"}
        )
        with pytest.raises(AuthenticationError):
            http_client.get("/test")

    def test_404_raises_not_found(
        self, http_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            status_code=404, json={"detail": "Not found"}
        )
        with pytest.raises(NotFoundError):
            http_client.get("/vulnerabilities/nonexistent")

    def test_422_raises_validation(
        self, http_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            status_code=422,
            json={"detail": [{"msg": "bad param"}]},
        )
        with pytest.raises(ValidationError):
            http_client.get("/test")

    def test_429_raises_rate_limit(
        self, http_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(
            status_code=429, json={"detail": "Too many requests"}
        )
        with pytest.raises(RateLimitError):
            http_client.get("/test")
