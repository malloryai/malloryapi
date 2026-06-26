"""Software extensions resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Extensions(SyncResource):
    _path = "/extensions"

    def list(
        self,
        *,
        filter: str | None = None,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            filter=filter,
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            **kwargs,
        )

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def configurations(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(identifier, "configurations", params=params)
        return _parse_paginated(data)

    def mentions(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
            "filter": filter,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(identifier, "mentions", params=params)
        return _parse_paginated(data)


class AsyncExtensions(AsyncResource):
    _path = "/extensions"

    async def list(
        self,
        *,
        filter: str | None = None,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            filter=filter,
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            **kwargs,
        )

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def configurations(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(identifier, "configurations", params=params)
        return _parse_paginated(data)

    async def mentions(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
            "filter": filter,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(identifier, "mentions", params=params)
        return _parse_paginated(data)
