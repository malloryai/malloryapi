"""Assets resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Assets(SyncResource):
    _path = "/assets"

    def exposure_check(self, data: dict[str, Any]) -> Any:
        return self._post(f"{self._path}/exposure-check", json=data)

    def presence_check(self, data: dict[str, Any]) -> Any:
        return self._post(f"{self._path}/presence-check", json=data)

    def _inventory(
        self, kind: str, offset: int, limit: int, **kwargs: Any
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._http.get(f"{self._path}/inventory/{kind}", params=params)
        return _parse_paginated(data)

    def inventory_hosts(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return self._inventory("hosts", offset, limit, **kwargs)

    def inventory_software(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return self._inventory("software", offset, limit, **kwargs)

    def inventory_users(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return self._inventory("users", offset, limit, **kwargs)

    def inventory_repositories(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return self._inventory("repositories", offset, limit, **kwargs)

    def inventory_cloud_resources(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return self._inventory("cloud_resources", offset, limit, **kwargs)

    def inventory_vulnerability_instances(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return self._inventory("vulnerability_instances", offset, limit, **kwargs)

    def profile(self) -> dict[str, Any]:
        return self._http.get(f"{self._path}/profile")

    def profile_for(self, entity_type: str) -> dict[str, Any]:
        return self._http.get(f"{self._path}/profile/{quote(entity_type, safe='')}")

    def vulnerabilities(
        self,
        *,
        vulnerability_uuid: str | None = None,
        status: str | None = None,
        asset_type: str | None = None,
        asset_uuid: str | None = None,
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "vulnerability_uuid": vulnerability_uuid,
            "status": status,
            "asset_type": asset_type,
            "asset_uuid": asset_uuid,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._http.get(f"{self._path}/vulnerabilities", params=params)
        return _parse_paginated(data)

    def upload(self, data: dict[str, Any]) -> Any:
        return self._post(f"{self._path}/upload", json=data)

    def uploads(
        self,
        *,
        status: str | None = None,
        data_type: str | None = None,
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "status": status,
            "data_type": data_type,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._http.get(f"{self._path}/uploads", params=params)
        return _parse_paginated(data)

    def upload_status(self, upload_uuid: str) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/uploads/{quote(upload_uuid, safe='')}/status"
        )

    def upload_retry(self, upload_uuid: str) -> Any:
        return self._post(f"{self._path}/uploads/{quote(upload_uuid, safe='')}/retry")


class AsyncAssets(AsyncResource):
    _path = "/assets"

    async def exposure_check(self, data: dict[str, Any]) -> Any:
        return await self._post(f"{self._path}/exposure-check", json=data)

    async def presence_check(self, data: dict[str, Any]) -> Any:
        return await self._post(f"{self._path}/presence-check", json=data)

    async def _inventory(
        self, kind: str, offset: int, limit: int, **kwargs: Any
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._http.get(f"{self._path}/inventory/{kind}", params=params)
        return _parse_paginated(data)

    async def inventory_hosts(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._inventory("hosts", offset, limit, **kwargs)

    async def inventory_software(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._inventory("software", offset, limit, **kwargs)

    async def inventory_users(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._inventory("users", offset, limit, **kwargs)

    async def inventory_repositories(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._inventory("repositories", offset, limit, **kwargs)

    async def inventory_cloud_resources(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._inventory("cloud_resources", offset, limit, **kwargs)

    async def inventory_vulnerability_instances(
        self, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._inventory("vulnerability_instances", offset, limit, **kwargs)

    async def profile(self) -> dict[str, Any]:
        return await self._http.get(f"{self._path}/profile")

    async def profile_for(self, entity_type: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/profile/{quote(entity_type, safe='')}"
        )

    async def vulnerabilities(
        self,
        *,
        vulnerability_uuid: str | None = None,
        status: str | None = None,
        asset_type: str | None = None,
        asset_uuid: str | None = None,
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "vulnerability_uuid": vulnerability_uuid,
            "status": status,
            "asset_type": asset_type,
            "asset_uuid": asset_uuid,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._http.get(f"{self._path}/vulnerabilities", params=params)
        return _parse_paginated(data)

    async def upload(self, data: dict[str, Any]) -> Any:
        return await self._post(f"{self._path}/upload", json=data)

    async def uploads(
        self,
        *,
        status: str | None = None,
        data_type: str | None = None,
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "status": status,
            "data_type": data_type,
            "offset": offset,
            "limit": limit,
            **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._http.get(f"{self._path}/uploads", params=params)
        return _parse_paginated(data)

    async def upload_status(self, upload_uuid: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/uploads/{quote(upload_uuid, safe='')}/status"
        )

    async def upload_retry(self, upload_uuid: str) -> Any:
        return await self._post(
            f"{self._path}/uploads/{quote(upload_uuid, safe='')}/retry"
        )
