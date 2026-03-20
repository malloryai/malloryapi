"""Dashboards resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Dashboards(SyncResource):
    _path = "/dashboards"

    def current_events(
        self,
        *,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "sort": sort, "order": order,
            "offset": offset, "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._http.get(
            f"{self._path}/current-events", params=params
        )
        return _parse_paginated(data)

    def vulnerabilities(
        self, *, limit: int = 24, **kwargs: Any
    ) -> dict[str, Any]:
        params = {"limit": limit, **kwargs}
        return self._http.get(
            f"{self._path}/vulnerabilities", params=params
        )

    def latest(self, report_type: str) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/{report_type}/latest"
        )

    def get(self, report_uuid: str) -> dict[str, Any]:
        return self._get(report_uuid)


class AsyncDashboards(AsyncResource):
    _path = "/dashboards"

    async def current_events(
        self,
        *,
        sort: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "sort": sort, "order": order,
            "offset": offset, "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._http.get(
            f"{self._path}/current-events", params=params
        )
        return _parse_paginated(data)

    async def vulnerabilities(
        self, *, limit: int = 24, **kwargs: Any
    ) -> dict[str, Any]:
        params = {"limit": limit, **kwargs}
        return await self._http.get(
            f"{self._path}/vulnerabilities", params=params
        )

    async def latest(self, report_type: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/{report_type}/latest"
        )

    async def get(self, report_uuid: str) -> dict[str, Any]:
        return await self._get(report_uuid)
