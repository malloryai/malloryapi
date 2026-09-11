"""Findings and external-ticket resources."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Findings(SyncResource):
    _path = "/findings"

    def list(
        self,
        *,
        where: str | None = None,
        thread_uuid: str | None = None,
        search: str | None = None,
        sort: str = "updated_at",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            where=where,
            thread_uuid=thread_uuid,
            search=search,
            sort=sort,
            order=order,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def batch_update(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._http.patch(self._path, json=data)

    def get(self, uuid: str) -> dict[str, Any]:
        return self._get(uuid)

    def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._patch(uuid, json=data)

    def delete(self, uuid: str) -> Any:
        return self._delete(uuid)

    def tickets(
        self,
        *,
        finding_uuid: str | None = None,
        provider: str | None = None,
        mcp_server_uuid: str | None = None,
        state: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "finding_uuid": finding_uuid,
            "provider": provider,
            "mcp_server_uuid": mcp_server_uuid,
            "state": state,
            "sort": sort,
            "order": order,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {key: value for key, value in params.items() if value is not None}
        data = self._http.get(f"{self._path}/tickets", params=params)
        return _parse_paginated(data)

    def create_ticket(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(f"{self._path}/tickets", json=data)

    def ticket_connections(self) -> list[dict[str, Any]]:
        return self._http.get(f"{self._path}/tickets/connections")

    def ticket_connection(self, mcp_server_uuid: str) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/tickets/connections/"
            f"{quote(mcp_server_uuid, safe='')}"
        )

    def lookup_ticket(
        self,
        *,
        mcp_server_uuid: str,
        url: str | None = None,
        external_id: str | None = None,
        provider: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        params = {
            "mcp_server_uuid": mcp_server_uuid,
            "url": url,
            "external_id": external_id,
            "provider": provider,
            **kwargs,
        }
        params = {key: value for key, value in params.items() if value is not None}
        return self._http.get(f"{self._path}/tickets/lookup", params=params)

    def get_ticket(self, uuid: str) -> dict[str, Any]:
        return self._http.get(f"{self._path}/tickets/{quote(uuid, safe='')}")

    def delete_ticket(self, uuid: str) -> Any:
        return self._http.delete(f"{self._path}/tickets/{quote(uuid, safe='')}")

    def refresh_ticket(self, uuid: str) -> dict[str, Any]:
        return self._post(f"{self._path}/tickets/{quote(uuid, safe='')}/refresh")

    def attach_findings(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(
            f"{self._path}/tickets/{quote(uuid, safe='')}/findings", json=data
        )

    def detach_finding(self, uuid: str, finding_uuid: str) -> Any:
        return self._http.delete(
            f"{self._path}/tickets/{quote(uuid, safe='')}/findings/"
            f"{quote(finding_uuid, safe='')}"
        )


class AsyncFindings(AsyncResource):
    _path = "/findings"

    async def list(
        self,
        *,
        where: str | None = None,
        thread_uuid: str | None = None,
        search: str | None = None,
        sort: str = "updated_at",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            where=where,
            thread_uuid=thread_uuid,
            search=search,
            sort=sort,
            order=order,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def batch_update(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(self._path, json=data)

    async def get(self, uuid: str) -> dict[str, Any]:
        return await self._get(uuid)

    async def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._patch(uuid, json=data)

    async def delete(self, uuid: str) -> Any:
        return await self._delete(uuid)

    async def tickets(
        self,
        *,
        finding_uuid: str | None = None,
        provider: str | None = None,
        mcp_server_uuid: str | None = None,
        state: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "finding_uuid": finding_uuid,
            "provider": provider,
            "mcp_server_uuid": mcp_server_uuid,
            "state": state,
            "sort": sort,
            "order": order,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {key: value for key, value in params.items() if value is not None}
        data = await self._http.get(f"{self._path}/tickets", params=params)
        return _parse_paginated(data)

    async def create_ticket(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(f"{self._path}/tickets", json=data)

    async def ticket_connections(self) -> list[dict[str, Any]]:
        return await self._http.get(f"{self._path}/tickets/connections")

    async def ticket_connection(self, mcp_server_uuid: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/tickets/connections/"
            f"{quote(mcp_server_uuid, safe='')}"
        )

    async def lookup_ticket(
        self,
        *,
        mcp_server_uuid: str,
        url: str | None = None,
        external_id: str | None = None,
        provider: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        params = {
            "mcp_server_uuid": mcp_server_uuid,
            "url": url,
            "external_id": external_id,
            "provider": provider,
            **kwargs,
        }
        params = {key: value for key, value in params.items() if value is not None}
        return await self._http.get(f"{self._path}/tickets/lookup", params=params)

    async def get_ticket(self, uuid: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/tickets/{quote(uuid, safe='')}"
        )

    async def delete_ticket(self, uuid: str) -> Any:
        return await self._http.delete(
            f"{self._path}/tickets/{quote(uuid, safe='')}"
        )

    async def refresh_ticket(self, uuid: str) -> dict[str, Any]:
        return await self._post(
            f"{self._path}/tickets/{quote(uuid, safe='')}/refresh"
        )

    async def attach_findings(
        self, uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._post(
            f"{self._path}/tickets/{quote(uuid, safe='')}/findings", json=data
        )

    async def detach_finding(self, uuid: str, finding_uuid: str) -> Any:
        return await self._http.delete(
            f"{self._path}/tickets/{quote(uuid, safe='')}/findings/"
            f"{quote(finding_uuid, safe='')}"
        )
