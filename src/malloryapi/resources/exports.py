"""Exports resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Exports(SyncResource):
    _path = "/exports"

    def list(self, **kwargs: Any) -> PaginatedResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = self._http.get(self._path, params=params)
        return _parse_paginated(data)

    def history(self, **kwargs: Any) -> PaginatedResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = self._http.get(
            f"{self._path}/history", params=params
        )
        return _parse_paginated(data)

    def latest(self, **kwargs: Any) -> dict[str, Any]:
        params = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.get(
            f"{self._path}/latest", params=params
        )

    def get(self, uuid: str, **kwargs: Any) -> dict[str, Any]:
        params = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.get(
            f"{self._path}/{uuid}", params=params
        )


class AsyncExports(AsyncResource):
    _path = "/exports"

    async def list(self, **kwargs: Any) -> PaginatedResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._http.get(self._path, params=params)
        return _parse_paginated(data)

    async def history(self, **kwargs: Any) -> PaginatedResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._http.get(
            f"{self._path}/history", params=params
        )
        return _parse_paginated(data)

    async def latest(self, **kwargs: Any) -> dict[str, Any]:
        params = {k: v for k, v in kwargs.items() if v is not None}
        return await self._http.get(
            f"{self._path}/latest", params=params
        )

    async def get(self, uuid: str, **kwargs: Any) -> dict[str, Any]:
        params = {k: v for k, v in kwargs.items() if v is not None}
        return await self._http.get(
            f"{self._path}/{uuid}", params=params
        )
