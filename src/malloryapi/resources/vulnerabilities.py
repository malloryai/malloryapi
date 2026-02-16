"""Vulnerabilities resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    TrendingPeriod,
)


class Vulnerabilities(SyncResource):
    _path = "/vulnerabilities"

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

    def exploited(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        data = self._http.get(
            f"{self._path}/exploited",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        from malloryapi.resources._base import _parse_paginated
        return _parse_paginated(data)

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def export(self, identifier: str) -> dict[str, Any]:
        return self._sub(identifier, "export")

    def configurations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(identifier, "configurations", params=kwargs)

    def detection_signatures(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "detection_signatures", params=kwargs
        )

    def exploits(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "exploits", params=kwargs)

    def exploitations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(identifier, "exploitations", params=kwargs)

    def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "mentions", params=kwargs)

    def products(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "products", params=kwargs)

    def advisories(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(
            identifier, "technology_product_advisories",
            params=kwargs,
        )

    def observables(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "observables", params=kwargs)

    def used_by_malware(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "used_by_malware", params=kwargs
        )

    def enrich(self, identifier: str) -> dict[str, Any]:
        return self._http.post(
            f"{self._path}/{identifier}/enrich"
        )


class AsyncVulnerabilities(AsyncResource):
    _path = "/vulnerabilities"

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

    async def exploited(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        data = await self._http.get(
            f"{self._path}/exploited",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        from malloryapi.resources._base import _parse_paginated
        return _parse_paginated(data)

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def export(self, identifier: str) -> dict[str, Any]:
        return await self._sub(identifier, "export")

    async def configurations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "configurations", params=kwargs
        )

    async def detection_signatures(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "detection_signatures", params=kwargs
        )

    async def exploits(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "exploits", params=kwargs
        )

    async def exploitations(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "exploitations", params=kwargs
        )

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

    async def advisories(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "technology_product_advisories",
            params=kwargs,
        )

    async def observables(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "observables", params=kwargs
        )

    async def used_by_malware(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "used_by_malware", params=kwargs
        )

    async def enrich(self, identifier: str) -> dict[str, Any]:
        return await self._http.post(
            f"{self._path}/{identifier}/enrich"
        )
