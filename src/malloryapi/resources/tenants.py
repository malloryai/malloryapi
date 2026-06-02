"""Tenants resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Tenants(SyncResource):
    _path = "/tenants"

    def list(self, *, offset: int = 0, limit: int = 50) -> PaginatedResponse:
        return self._list(offset=offset, limit=limit)

    def users(
        self, tenant_uuid: str, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(tenant_uuid, "users", params=params)
        return _parse_paginated(data)


class AsyncTenants(AsyncResource):
    _path = "/tenants"

    async def list(self, *, offset: int = 0, limit: int = 50) -> PaginatedResponse:
        return await self._list(offset=offset, limit=limit)

    async def users(
        self, tenant_uuid: str, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(tenant_uuid, "users", params=params)
        return _parse_paginated(data)
