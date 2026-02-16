"""Attack patterns resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    TrendingPeriod,
)


class AttackPatterns(SyncResource):
    _path = "/attack_patterns"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            **kwargs,
        )

    def trending(
        self, *, period: TrendingPeriod = "7d", **kwargs: Any
    ) -> PaginatedResponse:
        return self.list(sort=f"trending_{period}", **kwargs)

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "mentions", params=kwargs)

    def threat_actors(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "threat_actors", params=kwargs
        )

    def malware(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "malware", params=kwargs)


class AsyncAttackPatterns(AsyncResource):
    _path = "/attack_patterns"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            **kwargs,
        )

    async def trending(
        self, *, period: TrendingPeriod = "7d", **kwargs: Any
    ) -> PaginatedResponse:
        return await self.list(sort=f"trending_{period}", **kwargs)

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

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
            identifier, "threat_actors", params=kwargs
        )

    async def malware(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "malware", params=kwargs
        )
