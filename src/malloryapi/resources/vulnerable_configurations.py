"""Vulnerable technology product configuration sets resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class VulnerableConfigurations(SyncResource):
    _path = "/vulnerable_technology_product_configuration_sets"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
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

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def by_configuration(
        self, configuration_uuid: str
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/by-configuration/{configuration_uuid}"
        )

    def by_vulnerability(
        self, vulnerability_uuid: str
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/by-vulnerability/{vulnerability_uuid}"
        )

    def search(
        self, query: dict[str, Any], **kwargs: Any
    ) -> PaginatedResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = self._http.post(
            f"{self._path}/search", json=query, params=params
        )
        return _parse_paginated(data)


class AsyncVulnerableConfigurations(AsyncResource):
    _path = "/vulnerable_technology_product_configuration_sets"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
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

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def by_configuration(
        self, configuration_uuid: str
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/by-configuration/{configuration_uuid}"
        )

    async def by_vulnerability(
        self, vulnerability_uuid: str
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/by-vulnerability/{vulnerability_uuid}"
        )

    async def search(
        self, query: dict[str, Any], **kwargs: Any
    ) -> PaginatedResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._http.post(
            f"{self._path}/search", json=query, params=params
        )
        return _parse_paginated(data)
