"""Extensions resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
)


class Extensions(SyncResource):
    _path = "/extensions"

    def list(
        self,
        *,
        filter: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 100,
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

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def configurations(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "configurations", params=kwargs)

    def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "mentions", params=kwargs)


class AsyncExtensions(AsyncResource):
    _path = "/extensions"

    async def list(
        self,
        *,
        filter: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 100,
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

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def configurations(self, identifier: str, **kwargs: Any) -> Any:
        return await self._sub(identifier, "configurations", params=kwargs)

    async def mentions(self, identifier: str, **kwargs: Any) -> Any:
        return await self._sub(identifier, "mentions", params=kwargs)
