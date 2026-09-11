"""Observable sightings resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import AsyncResource, SyncResource


class Sightings(SyncResource):
    _path = "/sightings"

    def list(
        self,
        *,
        observable_type: str | None = None,
        observable_name: str | None = None,
        source: str | None = None,
        matched_at__gte: str | None = None,
        matched_at__lt: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            observable_type=observable_type,
            observable_name=observable_name,
            source=source,
            matched_at__gte=matched_at__gte,
            matched_at__lt=matched_at__lt,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def bulk(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(f"{self._path}/bulk", json=data)


class AsyncSightings(AsyncResource):
    _path = "/sightings"

    async def list(
        self,
        *,
        observable_type: str | None = None,
        observable_name: str | None = None,
        source: str | None = None,
        matched_at__gte: str | None = None,
        matched_at__lt: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            observable_type=observable_type,
            observable_name=observable_name,
            source=source,
            matched_at__gte=matched_at__gte,
            matched_at__lt=matched_at__lt,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def bulk(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(f"{self._path}/bulk", json=data)
