"""Integrations resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
)


class Integrations(SyncResource):
    _path = "/integrations"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 500,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(offset=offset, limit=limit, filter=filter, **kwargs)

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def get(self, integration_uuid: str) -> dict[str, Any]:
        return self._get(integration_uuid)

    def update(self, integration_uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._patch(integration_uuid, json=data)

    def delete(self, integration_uuid: str, *, force: bool = False) -> Any:
        params = {"force": force} if force else None
        return self._http.delete(
            f"{self._path}/{quote(integration_uuid, safe='')}", params=params
        )

    def capabilities(self) -> Any:
        return self._http.get(f"{self._path}/meta/capabilities")

    def schemas(self) -> Any:
        return self._http.get(f"{self._path}/meta/schemas")

    def run_action(
        self,
        integration_uuid: str,
        action: str,
        data: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.post(
            f"{self._path}/{quote(integration_uuid, safe='')}"
            f"/actions/{quote(action, safe='')}",
            json=data,
        )


class AsyncIntegrations(AsyncResource):
    _path = "/integrations"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 500,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(offset=offset, limit=limit, filter=filter, **kwargs)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def get(self, integration_uuid: str) -> dict[str, Any]:
        return await self._get(integration_uuid)

    async def update(
        self, integration_uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._patch(integration_uuid, json=data)

    async def delete(self, integration_uuid: str, *, force: bool = False) -> Any:
        params = {"force": force} if force else None
        return await self._http.delete(
            f"{self._path}/{quote(integration_uuid, safe='')}", params=params
        )

    async def capabilities(self) -> Any:
        return await self._http.get(f"{self._path}/meta/capabilities")

    async def schemas(self) -> Any:
        return await self._http.get(f"{self._path}/meta/schemas")

    async def run_action(
        self,
        integration_uuid: str,
        action: str,
        data: dict[str, Any] | None = None,
    ) -> Any:
        return await self._http.post(
            f"{self._path}/{quote(integration_uuid, safe='')}"
            f"/actions/{quote(action, safe='')}",
            json=data,
        )
