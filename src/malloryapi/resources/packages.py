"""Packages resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Packages(SyncResource):
    _path = "/packages"

    def list(
        self,
        *,
        filter: str | None = None,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        include_merged: bool | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            filter=filter,
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            include_merged=include_merged,
            **kwargs,
        )

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def compromises(
        self,
        identifier: str,
        *,
        compromise_type: str | None = None,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
    ) -> PaginatedResponse:
        params = {
            "compromise_type": compromise_type,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(identifier, "compromises", params=params)
        return _parse_paginated(data)

    def configurations(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
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
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
            "filter": filter,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(identifier, "mentions", params=params)
        return _parse_paginated(data)


class AsyncPackages(AsyncResource):
    _path = "/packages"

    async def list(
        self,
        *,
        filter: str | None = None,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
        include_merged: bool | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            filter=filter,
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            include_merged=include_merged,
            **kwargs,
        )

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def compromises(
        self,
        identifier: str,
        *,
        compromise_type: str | None = None,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
    ) -> PaginatedResponse:
        params = {
            "compromise_type": compromise_type,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(identifier, "compromises", params=params)
        return _parse_paginated(data)

    async def configurations(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 50,
        sort: str | None = None,
        order: str | None = None,
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
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
    ) -> PaginatedResponse:
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
            "filter": filter,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(identifier, "mentions", params=params)
        return _parse_paginated(data)
