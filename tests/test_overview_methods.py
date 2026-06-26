"""Tests for the *_overview relationship sub-endpoints."""

import pytest
from pytest_httpx import HTTPXMock

from malloryapi import AsyncMalloryApi, MalloryApi

ID = "x-1"

# (resource attribute, method name, expected path fragment)
OVERVIEW_CASES = [
    ("threat_actors", "attack_patterns_overview",
     "/actors/x-1/attack_patterns/overview"),
    ("threat_actors", "exploitations_overview",
     "/actors/x-1/exploitations/overview"),
    ("threat_actors", "malware_overview",
     "/actors/x-1/malware/overview"),
    ("threat_actors", "source_geographies_overview",
     "/actors/x-1/source-geographies/overview"),
    ("threat_actors", "target_geographies_overview",
     "/actors/x-1/target-geographies/overview"),
    ("threat_actors", "target_industries_overview",
     "/actors/x-1/target-industries/overview"),
    ("attack_patterns", "malware_overview",
     "/attack_patterns/x-1/malware/overview"),
    ("attack_patterns", "threat_actors_overview",
     "/attack_patterns/x-1/threat_actors/overview"),
    ("breaches", "attack_patterns_overview",
     "/breaches/x-1/attack-patterns/overview"),
    ("breaches", "malware_overview",
     "/breaches/x-1/malware/overview"),
    ("breaches", "threat_actors_overview",
     "/breaches/x-1/threat-actors/overview"),
    ("malware", "attack_patterns_overview",
     "/malware/x-1/attack_patterns/overview"),
    ("malware", "threat_actors_overview",
     "/malware/x-1/threat_actors/overview"),
    ("malware", "vulnerabilities_overview",
     "/malware/x-1/vulnerabilities/overview"),
    ("vulnerabilities", "malware_overview",
     "/vulnerabilities/x-1/malware/overview"),
    ("vulnerabilities", "threat_actors_overview",
     "/vulnerabilities/x-1/threat_actors/overview"),
]


@pytest.fixture
def client():
    c = MalloryApi(api_key="test-key")
    yield c
    c.close()


class TestOverviewMethods:
    @pytest.mark.parametrize("resource,method,fragment", OVERVIEW_CASES)
    def test_overview_path(
        self, client, httpx_mock: HTTPXMock, resource, method, fragment
    ):
        httpx_mock.add_response(json={"total": 0})
        getattr(getattr(client, resource), method)(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert fragment in str(request.url)

    def test_overview_forwards_kwargs(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"total": 0})
        client.threat_actors.malware_overview(ID, period="30d")
        request = httpx_mock.get_request()
        assert request.url.params["period"] == "30d"

    @pytest.mark.parametrize("resource,method,fragment", OVERVIEW_CASES)
    async def test_async_overview_path(
        self, httpx_mock: HTTPXMock, resource, method, fragment
    ):
        httpx_mock.add_response(json={"total": 0})
        c = AsyncMalloryApi(api_key="test-key")
        await getattr(getattr(c, resource), method)(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert fragment in str(request.url)
        await c.aclose()
