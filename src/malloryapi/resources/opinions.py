"""Opinions resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Opinions(SyncResource):
    _path = "/opinions"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            scope=scope, **kwargs,
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def get(self, uuid: str) -> dict[str, Any]:
        return self._get(uuid)

    def update(
        self, uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return self._patch(uuid, json=data)

    def delete(self, uuid: str) -> Any:
        return self._delete(uuid)

    def grouped(
        self,
        *,
        type: str | None = None,
        verdict: str | None = None,
        source: str | None = None,
        observable_name: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 50,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "type": type, "verdict": verdict,
            "source": source, "observable_name": observable_name,
            "sort": sort, "order": order,
            "offset": offset, "limit": limit,
            "scope": scope, **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._http.get(f"{self._path}/grouped", params=params)
        return _parse_paginated(data)


class AsyncOpinions(AsyncResource):
    _path = "/opinions"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            scope=scope, **kwargs,
        )

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def get(self, uuid: str) -> dict[str, Any]:
        return await self._get(uuid)

    async def update(
        self, uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._patch(uuid, json=data)

    async def delete(self, uuid: str) -> Any:
        return await self._delete(uuid)

    async def grouped(
        self,
        *,
        type: str | None = None,
        verdict: str | None = None,
        source: str | None = None,
        observable_name: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 50,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "type": type, "verdict": verdict,
            "source": source, "observable_name": observable_name,
            "sort": sort, "order": order,
            "offset": offset, "limit": limit,
            "scope": scope, **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._http.get(
            f"{self._path}/grouped", params=params
        )
        return _parse_paginated(data)
