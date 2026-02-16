"""Tests for client construction and resource access."""

import pytest

from malloryapi import AsyncMalloryApi, MalloryApi
from malloryapi.exceptions import AuthenticationError


class TestMalloryApiConstruction:
    def test_creates_with_api_key(self):
        client = MalloryApi(api_key="test-key")
        assert client.vulnerabilities is not None
        assert client.threat_actors is not None
        assert client.stories is not None
        client.close()

    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.delenv("MALLORY_API_KEY", raising=False)
        with pytest.raises(AuthenticationError, match="No API key"):
            MalloryApi()

    def test_reads_from_env(self, monkeypatch):
        monkeypatch.setenv("MALLORY_API_KEY", "env-key")
        client = MalloryApi()
        assert client._http is not None
        client.close()

    def test_context_manager(self):
        with MalloryApi(api_key="test-key") as client:
            assert client.vulnerabilities is not None

    def test_all_resources_present(self):
        client = MalloryApi(api_key="test-key")
        resources = [
            "vulnerabilities", "threat_actors", "malware",
            "exploits", "exploitations", "organizations",
            "products", "attack_patterns", "breaches",
            "detection_signatures", "advisories", "weaknesses",
            "stories", "references", "sources",
            "content_chunks", "mentions", "search",
        ]
        for name in resources:
            assert hasattr(client, name), f"Missing: {name}"
        client.close()


class TestAsyncMalloryApiConstruction:
    def test_creates_with_api_key(self):
        client = AsyncMalloryApi(api_key="test-key")
        assert client.vulnerabilities is not None
        assert client.threat_actors is not None

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with AsyncMalloryApi(api_key="test-key") as client:
            assert client.vulnerabilities is not None
