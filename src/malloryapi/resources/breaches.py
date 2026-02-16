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

    def organizations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "organizations", params=kwargs
        )


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

    async def organizations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "organizations", params=kwargs
        )
