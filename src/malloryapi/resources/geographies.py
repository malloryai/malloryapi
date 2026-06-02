"""Geographies resource."""

from __future__ import annotations

from typing import Any

from malloryapi.resources._base import AsyncResource, SyncResource


class Geographies(SyncResource):
    _path = "/geographies"

    def list(self) -> Any:
        return self._http.get(self._path)

    def get(self, code: str) -> dict[str, Any]:
        return self._get(code)


class AsyncGeographies(AsyncResource):
    _path = "/geographies"

    async def list(self) -> Any:
        return await self._http.get(self._path)

    async def get(self, code: str) -> dict[str, Any]:
        return await self._get(code)
