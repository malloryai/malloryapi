"""Stories resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Stories(SyncResource):
    _path = "/stories"

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

    def topics(self) -> list[dict[str, Any]]:
        return self._http.get(f"{self._path}/topics")

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def references(
        self, identifier: str, **kwargs: Any
    ) -> PaginatedResponse:
        data = self._sub(identifier, "references", params=kwargs)
        return _parse_paginated(data)

    def events(
        self, identifier: str, **kwargs: Any
    ) -> PaginatedResponse:
        data = self._sub(identifier, "events", params=kwargs)
        return _parse_paginated(data)

    def similar(
        self, identifier: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        return self._sub(identifier, "similar", params=kwargs)

    def entities(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(identifier, "entities", params=kwargs)

    def export(self, identifier: str) -> dict[str, Any]:
        return self._sub(identifier, "export")


class AsyncStories(AsyncResource):
    _path = "/stories"

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

    async def topics(self) -> list[dict[str, Any]]:
        return await self._http.get(f"{self._path}/topics")

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def references(
        self, identifier: str, **kwargs: Any
    ) -> PaginatedResponse:
        data = await self._sub(
            identifier, "references", params=kwargs
        )
        return _parse_paginated(data)

    async def events(
        self, identifier: str, **kwargs: Any
    ) -> PaginatedResponse:
        data = await self._sub(
            identifier, "events", params=kwargs
        )
        return _parse_paginated(data)

    async def similar(
        self, identifier: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        return await self._sub(
            identifier, "similar", params=kwargs
        )

    async def entities(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "entities", params=kwargs
        )

    async def export(self, identifier: str) -> dict[str, Any]:
        return await self._sub(identifier, "export")
