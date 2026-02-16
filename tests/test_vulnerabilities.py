"""Tests for the vulnerabilities resource."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import MalloryApi


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


VULN_LIST_RESPONSE = {
    "items": [
        {"uuid": "abc-123", "cve_id": "CVE-2024-1234"},
        {"uuid": "def-456", "cve_id": "CVE-2024-5678"},
    ],
    "total": 2,
    "offset": 0,
    "limit": 100,
}

VULN_DETAIL = {
    "uuid": "abc-123",
    "cve_id": "CVE-2024-1234",
    "description": "A test vulnerability",
    "cvss_base_score": 9.8,
}


class TestVulnerabilities:
    def test_list(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=VULN_LIST_RESPONSE)
        result = client.vulnerabilities.list(limit=10)
        assert len(result) == 2
        assert result.total == 2
        assert result[0]["cve_id"] == "CVE-2024-1234"

    def test_list_pagination(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=VULN_LIST_RESPONSE)
        client.vulnerabilities.list(
            offset=0, limit=10
        )
        request = httpx_mock.get_request()
        assert "offset=0" in str(request.url)
        assert "limit=10" in str(request.url)

    def test_trending(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=VULN_LIST_RESPONSE)
        client.vulnerabilities.trending(period="30d")
        request = httpx_mock.get_request()
        assert "sort=trending_30d" in str(request.url)

    def test_trending_default_period(
        self, client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(json=VULN_LIST_RESPONSE)
        client.vulnerabilities.trending()
        request = httpx_mock.get_request()
        assert "sort=trending_7d" in str(request.url)

    def test_get(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json=VULN_DETAIL)
        result = client.vulnerabilities.get("CVE-2024-1234")
        assert result["cve_id"] == "CVE-2024-1234"
        assert result["cvss_base_score"] == 9.8

    def test_export(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"export": "data"})
        result = client.vulnerabilities.export("abc-123")
        assert result == {"export": "data"}

    def test_exploits_sub(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.vulnerabilities.exploits("abc-123")
        request = httpx_mock.get_request()
        assert "/vulnerabilities/abc-123/exploits" in str(
            request.url
        )

    def test_mentions_sub(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.vulnerabilities.mentions("abc-123")
        request = httpx_mock.get_request()
        assert "/vulnerabilities/abc-123/mentions" in str(
            request.url
        )

    def test_enrich(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"status": "started"})
        client.vulnerabilities.enrich("abc-123")
        request = httpx_mock.get_request()
        assert request.method == "POST"
        assert "/vulnerabilities/abc-123/enrich" in str(
            request.url
        )
