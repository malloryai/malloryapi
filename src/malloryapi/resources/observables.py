"""Observables resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Observables(SyncResource):
    _path = "/observables"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            scope=scope, **kwargs,
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def get(self, uuid: str) -> dict[str, Any]:
        return self._get(uuid)

    def get_by_type_name(
        self,
        observable_type: str,
        name: str,
        *,
        scope: str | None = None,
    ) -> dict[str, Any]:
        params = {"scope": scope} if scope else None
        return self._http.get(
            f"{self._path}/{observable_type}/{name}", params=params
        )

    def update(
        self, uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return self._patch(uuid, json=data)

    def delete(self, uuid: str) -> Any:
        return self._delete(uuid)

    def opinions(
        self,
        uuid: str,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset, "limit": limit,
            "sort": sort, "order": order,
            "scope": scope, **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(uuid, "opinions", params=params)
        return _parse_paginated(data)

    def opinions_by_type_name(
        self,
        observable_type: str,
        name: str,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset, "limit": limit,
            "sort": sort, "order": order,
            "scope": scope, **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._http.get(
            f"{self._path}/{observable_type}/{name}/opinions",
            params=params,
        )
        return _parse_paginated(data)


class AsyncObservables(AsyncResource):
    _path = "/observables"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            scope=scope, **kwargs,
        )

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def get(self, uuid: str) -> dict[str, Any]:
        return await self._get(uuid)

    async def get_by_type_name(
        self,
        observable_type: str,
        name: str,
        *,
        scope: str | None = None,
    ) -> dict[str, Any]:
        params = {"scope": scope} if scope else None
        return await self._http.get(
            f"{self._path}/{observable_type}/{name}", params=params
        )

    async def update(
        self, uuid: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._patch(uuid, json=data)

    async def delete(self, uuid: str) -> Any:
        return await self._delete(uuid)

    async def opinions(
        self,
        uuid: str,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset, "limit": limit,
            "sort": sort, "order": order,
            "scope": scope, **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(uuid, "opinions", params=params)
        return _parse_paginated(data)

    async def opinions_by_type_name(
        self,
        observable_type: str,
        name: str,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        params = {
            "offset": offset, "limit": limit,
            "sort": sort, "order": order,
            "scope": scope, **kwargs,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._http.get(
            f"{self._path}/{observable_type}/{name}/opinions",
            params=params,
        )
        return _parse_paginated(data)
