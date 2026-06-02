"""Workspaces resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

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
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            filter=filter,
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
            "sort": sort,
            "order": order,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(uuid, "entities", params=params)
        return _parse_paginated(data)

    def add_entities(self, uuid: str, data: dict[str, Any]) -> Any:
        return self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_entities", json=data
        )

    def add_topics(self, uuid: str, data: dict[str, Any]) -> Any:
        return self._post(f"{self._path}/{quote(uuid, safe='')}/add_topics", json=data)

    def add_sources(self, uuid: str, data: dict[str, Any]) -> Any:
        return self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_sources", json=data
        )

    def members(self, uuid: str) -> Any:
        return self._sub(uuid, "members")

    def add_member(self, uuid: str, data: dict[str, Any]) -> Any:
        return self._post(
            f"{self._path}/{quote(uuid, safe='')}/members", json=data
        )

    def update_member(
        self, uuid: str, user_uuid: str, data: dict[str, Any]
    ) -> Any:
        return self._http.patch(
            f"{self._path}/{quote(uuid, safe='')}/members/"
            f"{quote(user_uuid, safe='')}",
            json=data,
        )

    def remove_member(self, uuid: str, user_uuid: str) -> Any:
        return self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/members/"
            f"{quote(user_uuid, safe='')}"
        )

    def sources(
        self, uuid: str, *, offset: int = 0, limit: int = 50
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit}
        data = self._sub(uuid, "sources", params=params)
        return _parse_paginated(data)

    def remove_source(self, uuid: str, source_uuid: str) -> Any:
        return self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/sources/"
            f"{quote(source_uuid, safe='')}"
        )

    def remove_entity(
        self, uuid: str, entity_type: str, entity_uuid: str
    ) -> Any:
        return self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/entities/"
            f"{quote(entity_type, safe='')}/{quote(entity_uuid, safe='')}"
        )

    def remove_topic(self, uuid: str, topic: str) -> Any:
        return self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/topics/"
            f"{quote(topic, safe='')}"
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
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            filter=filter,
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
            "sort": sort,
            "order": order,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(uuid, "entities", params=params)
        return _parse_paginated(data)

    async def add_entities(self, uuid: str, data: dict[str, Any]) -> Any:
        return await self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_entities", json=data
        )

    async def add_topics(self, uuid: str, data: dict[str, Any]) -> Any:
        return await self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_topics", json=data
        )

    async def add_sources(self, uuid: str, data: dict[str, Any]) -> Any:
        return await self._post(
            f"{self._path}/{quote(uuid, safe='')}/add_sources", json=data
        )

    async def members(self, uuid: str) -> Any:
        return await self._sub(uuid, "members")

    async def add_member(self, uuid: str, data: dict[str, Any]) -> Any:
        return await self._post(
            f"{self._path}/{quote(uuid, safe='')}/members", json=data
        )

    async def update_member(
        self, uuid: str, user_uuid: str, data: dict[str, Any]
    ) -> Any:
        return await self._http.patch(
            f"{self._path}/{quote(uuid, safe='')}/members/"
            f"{quote(user_uuid, safe='')}",
            json=data,
        )

    async def remove_member(self, uuid: str, user_uuid: str) -> Any:
        return await self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/members/"
            f"{quote(user_uuid, safe='')}"
        )

    async def sources(
        self, uuid: str, *, offset: int = 0, limit: int = 50
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit}
        data = await self._sub(uuid, "sources", params=params)
        return _parse_paginated(data)

    async def remove_source(self, uuid: str, source_uuid: str) -> Any:
        return await self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/sources/"
            f"{quote(source_uuid, safe='')}"
        )

    async def remove_entity(
        self, uuid: str, entity_type: str, entity_uuid: str
    ) -> Any:
        return await self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/entities/"
            f"{quote(entity_type, safe='')}/{quote(entity_uuid, safe='')}"
        )

    async def remove_topic(self, uuid: str, topic: str) -> Any:
        return await self._http.delete(
            f"{self._path}/{quote(uuid, safe='')}/topics/"
            f"{quote(topic, safe='')}"
        )
