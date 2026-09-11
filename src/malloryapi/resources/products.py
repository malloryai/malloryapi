"""Products (technology products) resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    TrendingPeriod,
    _parse_paginated,
)


class Products(SyncResource):
    _path = "/products"

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
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            filter=filter,
            **kwargs,
        )

    def trending(
        self, *, period: TrendingPeriod = "7d", **kwargs: Any
    ) -> PaginatedResponse:
        return self.list(sort=f"trending_{period}", **kwargs)

    def search(
        self,
        query: dict[str, Any],
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str = "created_at",
        order: str = "desc",
        **kwargs: Any,
    ) -> Any:
        return self._post(
            f"{self._path}/search",
            json=query,
            params={
                "offset": offset,
                "limit": limit,
                "sort": sort,
                "order": order,
                **kwargs,
            },
        )

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def export(
        self,
        identifier: str,
        *,
        relationships_created_after: str | None = None,
        relationships_created_before: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self._sub(
            identifier,
            "export",
            params={
                "relationships_created_after": relationships_created_after,
                "relationships_created_before": relationships_created_before,
                **kwargs,
            },
        )

    def similar(
        self,
        identifier: str,
        *,
        threshold: float = -1.0,
        offset: int = 0,
        limit: int = 10,
        **kwargs: Any,
    ) -> PaginatedResponse:
        data = self._sub(
            identifier,
            "similar",
            params={
                "threshold": threshold,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )
        return _parse_paginated(data)

    def advisories(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(
            identifier,
            "technology_product_advisories",
            params=kwargs,
        )

    def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "mentions", params=kwargs)

    def update(self, identifier: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._patch(identifier, json=data)

    def delete(self, identifier: str) -> Any:
        return self._delete(identifier)

    def enrich(self, identifier: str) -> dict[str, Any]:
        return self._http.post(f"{self._path}/{quote(identifier, safe='')}/enrich")


class AsyncProducts(AsyncResource):
    _path = "/products"

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
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            filter=filter,
            **kwargs,
        )

    async def trending(
        self, *, period: TrendingPeriod = "7d", **kwargs: Any
    ) -> PaginatedResponse:
        return await self.list(sort=f"trending_{period}", **kwargs)

    async def search(
        self,
        query: dict[str, Any],
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str = "created_at",
        order: str = "desc",
        **kwargs: Any,
    ) -> Any:
        return await self._post(
            f"{self._path}/search",
            json=query,
            params={
                "offset": offset,
                "limit": limit,
                "sort": sort,
                "order": order,
                **kwargs,
            },
        )

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def export(
        self,
        identifier: str,
        *,
        relationships_created_after: str | None = None,
        relationships_created_before: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self._sub(
            identifier,
            "export",
            params={
                "relationships_created_after": relationships_created_after,
                "relationships_created_before": relationships_created_before,
                **kwargs,
            },
        )

    async def similar(
        self,
        identifier: str,
        *,
        threshold: float = -1.0,
        offset: int = 0,
        limit: int = 10,
        **kwargs: Any,
    ) -> PaginatedResponse:
        data = await self._sub(
            identifier,
            "similar",
            params={
                "threshold": threshold,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )
        return _parse_paginated(data)

    async def advisories(self, identifier: str, **kwargs: Any) -> Any:
        return await self._sub(
            identifier,
            "technology_product_advisories",
            params=kwargs,
        )

    async def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return await self._sub(identifier, "mentions", params=kwargs)

    async def update(self, identifier: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._patch(identifier, json=data)

    async def delete(self, identifier: str) -> Any:
        return await self._delete(identifier)

    async def enrich(self, identifier: str) -> dict[str, Any]:
        return await self._http.post(
            f"{self._path}/{quote(identifier, safe='')}/enrich"
        )
