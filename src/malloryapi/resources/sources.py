"""Sources resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import AsyncResource, SyncResource


class Sources(SyncResource):
    _path = "/sources"

    def list(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        return self._list(offset=offset, limit=limit, **kwargs)

    def statistics(self, source: str) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/{source}/statistics"
        )


class AsyncSources(AsyncResource):
    _path = "/sources"

    async def list(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit, **kwargs
        )

    async def statistics(self, source: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/{source}/statistics"
        )
