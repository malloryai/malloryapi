"""Finding definitions resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import AsyncResource, SyncResource


class FindingDefinitions(SyncResource):
    _path = "/finding_definitions"

    def list(
        self,
        *,
        scope: str | None = None,
        where: str | None = None,
        include_deprecated: bool = False,
        sort: str = "title",
        order: str = "asc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            scope=scope,
            where=where,
            include_deprecated=include_deprecated,
            sort=sort,
            order=order,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post(json=data)

    def get(
        self, slug: str, *, scope: str | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        params = {"scope": scope, **kwargs}
        params = {key: value for key, value in params.items() if value is not None}
        return self._http.get(
            f"{self._path}/{quote(slug, safe='')}", params=params
        )

    def update(self, slug: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._http.patch(
            f"{self._path}/{quote(slug, safe='')}", json=data
        )

    def delete(self, slug: str) -> Any:
        return self._http.delete(f"{self._path}/{quote(slug, safe='')}")


class AsyncFindingDefinitions(AsyncResource):
    _path = "/finding_definitions"

    async def list(
        self,
        *,
        scope: str | None = None,
        where: str | None = None,
        include_deprecated: bool = False,
        sort: str = "title",
        order: str = "asc",
        offset: int = 0,
        limit: int = 50,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            scope=scope,
            where=where,
            include_deprecated=include_deprecated,
            sort=sort,
            order=order,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._post(json=data)

    async def get(
        self, slug: str, *, scope: str | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        params = {"scope": scope, **kwargs}
        params = {key: value for key, value in params.items() if value is not None}
        return await self._http.get(
            f"{self._path}/{quote(slug, safe='')}", params=params
        )

    async def update(self, slug: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(
            f"{self._path}/{quote(slug, safe='')}", json=data
        )

    async def delete(self, slug: str) -> Any:
        return await self._http.delete(f"{self._path}/{quote(slug, safe='')}")
