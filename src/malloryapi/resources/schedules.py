"""Schedules resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Schedules(SyncResource):
    _path = "/schedules"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        filter: str | None = None,
        uuid: str | None = None,
        status: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            offset=offset, limit=limit,
            filter=filter, uuid=uuid, status=status,
            **kwargs,
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def get(self, schedule_uuid: str) -> dict[str, Any]:
        return self._get(schedule_uuid)

    def update(
        self, schedule_uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return self._patch(schedule_uuid, json=data)

    def delete(self, schedule_uuid: str) -> Any:
        return self._delete(schedule_uuid)

    def executions(
        self,
        schedule_uuid: str,
        *,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        data = self._sub(
            schedule_uuid, "executions",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        return _parse_paginated(data)


class AsyncSchedules(AsyncResource):
    _path = "/schedules"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        filter: str | None = None,
        uuid: str | None = None,
        status: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit,
            filter=filter, uuid=uuid, status=status,
            **kwargs,
        )

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def get(self, schedule_uuid: str) -> dict[str, Any]:
        return await self._get(schedule_uuid)

    async def update(
        self, schedule_uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._patch(schedule_uuid, json=data)

    async def delete(self, schedule_uuid: str) -> Any:
        return await self._delete(schedule_uuid)

    async def executions(
        self,
        schedule_uuid: str,
        *,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        data = await self._sub(
            schedule_uuid, "executions",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        return _parse_paginated(data)
