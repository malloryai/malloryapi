"""Tests for overview sub-resource methods."""

import pytest
from pytest_httpx import HTTPXMock

ID = "ent-1"


class TestThreatActorsOverviews:
    def test_attack_patterns_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.threat_actors.attack_patterns_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/actors/ent-1/attack_patterns/overview" in str(request.url)

    def test_exploitations_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.threat_actors.exploitations_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/actors/ent-1/exploitations/overview" in str(request.url)

    def test_malware_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.threat_actors.malware_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/actors/ent-1/malware/overview" in str(request.url)

    def test_source_geographies_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.threat_actors.source_geographies_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/actors/ent-1/source-geographies/overview" in str(request.url)

    def test_target_geographies_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.threat_actors.target_geographies_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/actors/ent-1/target-geographies/overview" in str(request.url)

    def test_target_industries_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.threat_actors.target_industries_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/actors/ent-1/target-industries/overview" in str(request.url)

    @pytest.mark.asyncio
    async def test_attack_patterns_overview_async(
        self, async_client, httpx_mock: HTTPXMock
    ):
        httpx_mock.add_response(json={"items": []})
        await async_client.threat_actors.attack_patterns_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/actors/ent-1/attack_patterns/overview" in str(request.url)


class TestAttackPatternsOverviews:
    def test_malware_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.attack_patterns.malware_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/attack_patterns/ent-1/malware/overview" in str(request.url)

    def test_threat_actors_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.attack_patterns.threat_actors_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/attack_patterns/ent-1/threat_actors/overview" in str(request.url)


class TestBreachesOverviews:
    def test_attack_patterns_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.breaches.attack_patterns_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/breaches/ent-1/attack-patterns/overview" in str(request.url)

    def test_malware_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.breaches.malware_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/breaches/ent-1/malware/overview" in str(request.url)

    def test_threat_actors_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.breaches.threat_actors_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/breaches/ent-1/threat-actors/overview" in str(request.url)


class TestMalwareOverviews:
    def test_attack_patterns_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.malware.attack_patterns_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/malware/ent-1/attack_patterns/overview" in str(request.url)

    def test_threat_actors_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.malware.threat_actors_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/malware/ent-1/threat_actors/overview" in str(request.url)

    def test_vulnerabilities_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.malware.vulnerabilities_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/malware/ent-1/vulnerabilities/overview" in str(request.url)


class TestVulnerabilitiesOverviews:
    def test_malware_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.vulnerabilities.malware_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/vulnerabilities/ent-1/malware/overview" in str(request.url)

    def test_threat_actors_overview(self, client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        client.vulnerabilities.threat_actors_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/vulnerabilities/ent-1/threat_actors/overview" in str(request.url)

    @pytest.mark.asyncio
    async def test_malware_overview_async(self, async_client, httpx_mock: HTTPXMock):
        httpx_mock.add_response(json={"items": []})
        await async_client.vulnerabilities.malware_overview(ID)
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert "/vulnerabilities/ent-1/malware/overview" in str(request.url)
