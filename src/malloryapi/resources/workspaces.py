"""Workspaces resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Workspaces(SyncResource):
    _path = "/workspaces"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
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

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def get(self, uuid: str) -> dict[str, Any]:
        return self._get(uuid)

    def update(
        self, uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return self._put(uuid, json=data)

    def delete(self, uuid: str) -> Any:
        return self._delete(uuid)

    def entities(
        self,
        uuid: str,
        *,
        entity_type: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "entity_type": entity_type,
            "sort": sort, "order": order,
            "offset": offset, "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(uuid, "entities", params=params)
        return _parse_paginated(data)

    def add_entities(
        self, uuid: str, data: dict[str, Any]
    ) -> Any:
        return self._post(
            f"{self._path}/{uuid}/add_entities", json=data
        )

    def add_topics(
        self, uuid: str, data: dict[str, Any]
    ) -> Any:
        return self._post(
            f"{self._path}/{uuid}/add_topics", json=data
        )


class AsyncWorkspaces(AsyncResource):
    _path = "/workspaces"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
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

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def get(self, uuid: str) -> dict[str, Any]:
        return await self._get(uuid)

    async def update(
        self, uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._put(uuid, json=data)

    async def delete(self, uuid: str) -> Any:
        return await self._delete(uuid)

    async def entities(
        self,
        uuid: str,
        *,
        entity_type: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "entity_type": entity_type,
            "sort": sort, "order": order,
            "offset": offset, "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(uuid, "entities", params=params)
        return _parse_paginated(data)

    async def add_entities(
        self, uuid: str, data: dict[str, Any]
    ) -> Any:
        return await self._post(
            f"{self._path}/{uuid}/add_entities", json=data
        )

    async def add_topics(
        self, uuid: str, data: dict[str, Any]
    ) -> Any:
        return await self._post(
            f"{self._path}/{uuid}/add_topics", json=data
        )
