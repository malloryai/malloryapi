"""Tests for the assets resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


LIST_RESPONSE = {
    "items": [{"uuid": "h-1"}, {"uuid": "h-2"}],
    "total": 2,
    "offset": 0,
    "limit": 50,
}


class TestAssets:
    def test_inventory_hosts(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        result = client.assets.inventory_hosts(limit=10)
        request = httpx_mock.get_request()
        assert "/assets/inventory/hosts" in str(request.url)
        assert len(result) == 2
        assert result.total == 2

    def test_inventory_software(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        client.assets.inventory_software()
        request = httpx_mock.get_request()
        assert "/assets/inventory/software" in str(request.url)

    def test_vulnerabilities(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        client.assets.vulnerabilities(status="open")
        request = httpx_mock.get_request()
        assert "/assets/vulnerabilities" in str(request.url)
        assert "status=open" in str(request.url)

    def test_profile(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"hosts": 5})
        result = client.assets.profile()
        request = httpx_mock.get_request()
        assert "/assets/profile" in str(request.url)
        assert result == {"hosts": 5}

    def test_profile_for(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"count": 3})
        client.assets.profile_for("host")
        request = httpx_mock.get_request()
        assert "/assets/profile/host" in str(request.url)

    def test_exposure_check(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"matches": []})
        result = client.assets.exposure_check(
            {"entities": ["1.2.3.4"], "entity_types": ["ip_address"]}
        )
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/assets/exposure-check" in str(request.url)
        assert result == {"matches": []}

    def test_uploads(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=LIST_RESPONSE)
        client.assets.uploads(status="complete")
        request = httpx_mock.get_request()
        assert "/assets/uploads" in str(request.url)

    def test_upload_status(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"status": "complete"})
        client.assets.upload_status("up-1")
        request = httpx_mock.get_request()
        assert "/assets/uploads/up-1/status" in str(request.url)

    def test_upload_retry(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"status": "queued"})
        client.assets.upload_retry("up-1")
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/assets/uploads/up-1/retry" in str(request.url)
