"""Organizations resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    TrendingPeriod,
)


class Organizations(SyncResource):
    _path = "/organizations"

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

    def export(self, identifier: str) -> dict[str, Any]:
        return self._sub(identifier, "export")

    def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "mentions", params=kwargs)

    def products(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "products", params=kwargs)

    def breaches(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "breaches", params=kwargs)

    def enrich(self, identifier: str) -> dict[str, Any]:
        return self._http.post(
            f"{self._path}/{identifier}/enrich"
        )


class AsyncOrganizations(AsyncResource):
    _path = "/organizations"

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

    async def export(self, identifier: str) -> dict[str, Any]:
        return await self._sub(identifier, "export")

    async def mentions(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "mentions", params=kwargs
        )

    async def products(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "products", params=kwargs
        )

    async def breaches(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "breaches", params=kwargs
        )

    async def enrich(self, identifier: str) -> dict[str, Any]:
        return await self._http.post(
            f"{self._path}/{identifier}/enrich"
        )
