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


def _match_path(entity_type: str, entity_uuid: str) -> str:
    return (
        "/assets/matches/"
        f"{quote(entity_type, safe='')}/{quote(entity_uuid, safe='')}"
    )


def _matched_assets_path(
    entity_type: str, entity_uuid: str, source_table: str
) -> str:
    return (
        f"{_match_path(entity_type, entity_uuid)}/assets/"
        f"{quote(source_table, safe='')}"
    )


class Assets(SyncResource):
    _path = "/assets"

    def live_catalog(self, *, plugins: list[str] | None = None) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/live/catalog", params={"plugins": plugins}
        )

    def list_matches(
        self,
        *,
        sort: str = "asset_count",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/matches",
            params={
                "sort": sort,
                "order": order,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )

    def matches_summary(self) -> dict[str, Any]:
        return self._http.get(f"{self._path}/matches/summary")

    def list_vulnerability_matches(
        self,
        *,
        sort: str = "asset_count",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        trending_window: str = "1d",
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/matches/vulnerabilities",
            params={
                "sort": sort,
                "order": order,
                "offset": offset,
                "limit": limit,
                "trending_window": trending_window,
                **kwargs,
            },
        )

    def story_matches(self, story_uuid: str) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/matches/story/{quote(story_uuid, safe='')}/matches"
        )

    def get_match(self, entity_type: str, entity_uuid: str) -> dict[str, Any]:
        return self._http.get(_match_path(entity_type, entity_uuid))

    def matched_assets(
        self,
        entity_type: str,
        entity_uuid: str,
        source_table: str,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        return self._http.get(
            _matched_assets_path(entity_type, entity_uuid, source_table),
            params={"offset": offset, "limit": limit},
        )

    def query_matched_assets(
        self,
        entity_type: str,
        entity_uuid: str,
        source_table: str,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        return self._http.post(
            f"{_matched_assets_path(entity_type, entity_uuid, source_table)}/query",
            json=query,
        )

    def matched_assets_schema(
        self, entity_type: str, entity_uuid: str, source_table: str
    ) -> dict[str, Any]:
        return self._http.get(
            f"{_matched_assets_path(entity_type, entity_uuid, source_table)}/schema"
        )

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

    async def live_catalog(
        self, *, plugins: list[str] | None = None
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/live/catalog", params={"plugins": plugins}
        )

    async def list_matches(
        self,
        *,
        sort: str = "asset_count",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/matches",
            params={
                "sort": sort,
                "order": order,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )

    async def matches_summary(self) -> dict[str, Any]:
        return await self._http.get(f"{self._path}/matches/summary")

    async def list_vulnerability_matches(
        self,
        *,
        sort: str = "asset_count",
        order: str = "desc",
        offset: int = 0,
        limit: int = 50,
        trending_window: str = "1d",
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/matches/vulnerabilities",
            params={
                "sort": sort,
                "order": order,
                "offset": offset,
                "limit": limit,
                "trending_window": trending_window,
                **kwargs,
            },
        )

    async def story_matches(self, story_uuid: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/matches/story/{quote(story_uuid, safe='')}/matches"
        )

    async def get_match(
        self, entity_type: str, entity_uuid: str
    ) -> dict[str, Any]:
        return await self._http.get(_match_path(entity_type, entity_uuid))

    async def matched_assets(
        self,
        entity_type: str,
        entity_uuid: str,
        source_table: str,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        return await self._http.get(
            _matched_assets_path(entity_type, entity_uuid, source_table),
            params={"offset": offset, "limit": limit},
        )

    async def query_matched_assets(
        self,
        entity_type: str,
        entity_uuid: str,
        source_table: str,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{_matched_assets_path(entity_type, entity_uuid, source_table)}/query",
            json=query,
        )

    async def matched_assets_schema(
        self, entity_type: str, entity_uuid: str, source_table: str
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{_matched_assets_path(entity_type, entity_uuid, source_table)}/schema"
        )

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
