"""Breaches resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import AsyncResource, SyncResource


class Breaches(SyncResource):
    _path = "/breaches"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, **kwargs,
        )

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def export(
        self,
        identifier: str,
        *,
        relationships_created_after: str | None = None,
        relationships_created_before: str | None = None,
    ) -> dict[str, Any]:
        params = {
            "relationships_created_after": relationships_created_after,
            "relationships_created_before": relationships_created_before,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._sub(identifier, "export", params=params)

    def organizations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "organizations", params=kwargs
        )

    def attack_patterns(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "attack-patterns", params=kwargs
        )

    def attack_patterns_overview(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "attack-patterns/overview", params=kwargs
        )

    def malware(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "malware", params=kwargs)

    def malware_overview(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "malware/overview", params=kwargs
        )

    def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "mentions", params=kwargs)

    def threat_actors(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "threat-actors", params=kwargs
        )

    def threat_actors_overview(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "threat-actors/overview", params=kwargs
        )

    def delete(self, identifier: str) -> Any:
        return self._delete(identifier)


class AsyncBreaches(AsyncResource):
    _path = "/breaches"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, **kwargs,
        )

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def export(
        self,
        identifier: str,
        *,
        relationships_created_after: str | None = None,
        relationships_created_before: str | None = None,
    ) -> dict[str, Any]:
        params = {
            "relationships_created_after": relationships_created_after,
            "relationships_created_before": relationships_created_before,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return await self._sub(identifier, "export", params=params)

    async def organizations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "organizations", params=kwargs
        )

    async def attack_patterns(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "attack-patterns", params=kwargs
        )

    async def attack_patterns_overview(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "attack-patterns/overview", params=kwargs
        )

    async def malware(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "malware", params=kwargs
        )

    async def malware_overview(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "malware/overview", params=kwargs
        )

    async def mentions(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "mentions", params=kwargs
        )

    async def threat_actors(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "threat-actors", params=kwargs
        )

    async def threat_actors_overview(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "threat-actors/overview", params=kwargs
        )

    async def delete(self, identifier: str) -> Any:
        return await self._delete(identifier)
