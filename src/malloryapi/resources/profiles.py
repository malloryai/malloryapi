"""Profiles resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Profiles(SyncResource):
    _path = "/profiles"

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
            filter=filter,
            sort=sort,
            order=order,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def get(self, uuid: str) -> dict[str, Any]:
        return self._get(uuid)

    def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._put(uuid, json=data)

    def delete(self, uuid: str) -> Any:
        return self._delete(uuid)

    def add_entities(self, uuid: str, data: dict[str, Any]) -> Any:
        return self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_entities", json=data
        )

    def add_topics(self, uuid: str, data: dict[str, Any]) -> Any:
        return self._post(f"{self._path}/{quote(uuid, safe='')}/add_topics", json=data)

    def entities(
        self,
        uuid: str,
        *,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(uuid, "entities", params=params)
        return _parse_paginated(data)


class AsyncProfiles(AsyncResource):
    _path = "/profiles"

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
            filter=filter,
            sort=sort,
            order=order,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def get(self, uuid: str) -> dict[str, Any]:
        return await self._get(uuid)

    async def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._put(uuid, json=data)

    async def delete(self, uuid: str) -> Any:
        return await self._delete(uuid)

    async def add_entities(self, uuid: str, data: dict[str, Any]) -> Any:
        return await self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_entities", json=data
        )

    async def add_topics(self, uuid: str, data: dict[str, Any]) -> Any:
        return await self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_topics", json=data
        )

    async def entities(
        self,
        uuid: str,
        *,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(uuid, "entities", params=params)
        return _parse_paginated(data)
