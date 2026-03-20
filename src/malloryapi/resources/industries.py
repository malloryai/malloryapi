"""Industries resource."""

from __future__ import annotations

from typing import Any

from malloryapi.resources._base import AsyncResource, SyncResource


class Industries(SyncResource):
    _path = "/industries"

    def list(self) -> list[dict[str, Any]]:
        return self._http.get(self._path)

    def get(self, code: str) -> dict[str, Any]:
        return self._get(code)


class AsyncIndustries(AsyncResource):
    _path = "/industries"

    async def list(self) -> list[dict[str, Any]]:
        return await self._http.get(self._path)

    async def get(self, code: str) -> dict[str, Any]:
        return await self._get(code)
