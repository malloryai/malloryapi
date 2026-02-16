"""Main client classes for the Mallory API."""

from __future__ import annotations

from malloryapi._http import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    AsyncHttpClient,
    SyncHttpClient,
)
from malloryapi.resources.attack_patterns import (
    AsyncAttackPatterns,
    AttackPatterns,
)
from malloryapi.resources.breaches import AsyncBreaches, Breaches
from malloryapi.resources.content_chunks import (
    AsyncContentChunks,
    ContentChunks,
)
from malloryapi.resources.detection_signatures import (
    AsyncDetectionSignatures,
    DetectionSignatures,
)
from malloryapi.resources.exploitations import (
    AsyncExploitations,
    Exploitations,
)
from malloryapi.resources.exploits import AsyncExploits, Exploits
from malloryapi.resources.malware import AsyncMalware, Malware
from malloryapi.resources.mentions import AsyncMentions, Mentions
from malloryapi.resources.organizations import (
    AsyncOrganizations,
    Organizations,
)
from malloryapi.resources.products import AsyncProducts, Products
from malloryapi.resources.references import (
    AsyncReferences,
    References,
)
from malloryapi.resources.search import AsyncSearch, Search
from malloryapi.resources.sources import AsyncSources, Sources
from malloryapi.resources.stories import AsyncStories, Stories
from malloryapi.resources.technology_product_advisories import (
    AsyncTechnologyProductAdvisories,
    TechnologyProductAdvisories,
)
from malloryapi.resources.threat_actors import (
    AsyncThreatActors,
    ThreatActors,
)
from malloryapi.resources.vulnerabilities import (
    AsyncVulnerabilities,
    Vulnerabilities,
)
from malloryapi.resources.weaknesses import (
    AsyncWeaknesses,
    Weaknesses,
)


class MalloryApi:
    """Synchronous client for the Mallory threat intelligence API.

    Usage::

        from malloryapi import MalloryApi

        client = MalloryApi(api_key="sk-...")
        vulns = client.vulnerabilities.list(limit=10)
        actor = client.threat_actors.get("apt28-uuid")
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._http = SyncHttpClient(
            api_key=api_key, base_url=base_url, timeout=timeout
        )

        # Entities
        self.vulnerabilities = Vulnerabilities(self._http)
        self.threat_actors = ThreatActors(self._http)
        self.malware = Malware(self._http)
        self.exploits = Exploits(self._http)
        self.exploitations = Exploitations(self._http)
        self.organizations = Organizations(self._http)
        self.products = Products(self._http)
        self.attack_patterns = AttackPatterns(self._http)
        self.breaches = Breaches(self._http)
        self.detection_signatures = DetectionSignatures(self._http)
        self.advisories = TechnologyProductAdvisories(self._http)
        self.weaknesses = Weaknesses(self._http)

        # Content
        self.stories = Stories(self._http)
        self.references = References(self._http)
        self.sources = Sources(self._http)
        self.content_chunks = ContentChunks(self._http)

        # Analytics
        self.mentions = Mentions(self._http)
        self.search = Search(self._http)

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._http.close()

    def __enter__(self) -> MalloryApi:
        return self

    def __exit__(self, *args) -> None:
        self.close()


class AsyncMalloryApi:
    """Asynchronous client for the Mallory threat intelligence API.

    Usage::

        from malloryapi import AsyncMalloryApi

        async with AsyncMalloryApi(api_key="sk-...") as client:
            vulns = await client.vulnerabilities.list(limit=10)
            actor = await client.threat_actors.get("apt28-uuid")
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._http = AsyncHttpClient(
            api_key=api_key, base_url=base_url, timeout=timeout
        )

        # Entities
        self.vulnerabilities = AsyncVulnerabilities(self._http)
        self.threat_actors = AsyncThreatActors(self._http)
        self.malware = AsyncMalware(self._http)
        self.exploits = AsyncExploits(self._http)
        self.exploitations = AsyncExploitations(self._http)
        self.organizations = AsyncOrganizations(self._http)
        self.products = AsyncProducts(self._http)
        self.attack_patterns = AsyncAttackPatterns(self._http)
        self.breaches = AsyncBreaches(self._http)
        self.detection_signatures = AsyncDetectionSignatures(
            self._http
        )
        self.advisories = AsyncTechnologyProductAdvisories(
            self._http
        )
        self.weaknesses = AsyncWeaknesses(self._http)

        # Content
        self.stories = AsyncStories(self._http)
        self.references = AsyncReferences(self._http)
        self.sources = AsyncSources(self._http)
        self.content_chunks = AsyncContentChunks(self._http)

        # Analytics
        self.mentions = AsyncMentions(self._http)
        self.search = AsyncSearch(self._http)

    async def aclose(self) -> None:
        """Close the underlying HTTP connection."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncMalloryApi:
        return self

    async def __aexit__(self, *args) -> None:
        await self.aclose()
