"""Base resource classes for sync and async API access."""

from __future__ import annotations

from typing import Any, Literal

from malloryapi._http import AsyncHttpClient, SyncHttpClient
from malloryapi._types import PaginatedResponse

TrendingPeriod = Literal["1d", "7d", "30d"]


class SyncResource:
    """Base class for synchronous resource clients."""

    _path: str  # e.g. "/vulnerabilities"

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    # -- common helpers ------------------------------------------------

    def _list(
        self,
        params: dict[str, Any] | None = None,
        **extra: Any,
    ) -> PaginatedResponse:
        merged = {**(params or {}), **extra}
        merged = {k: v for k, v in merged.items() if v is not None}
        data = self._http.get(self._path, params=merged)
        return _parse_paginated(data)

    def _get(self, identifier: str) -> dict[str, Any]:
        return self._http.get(f"{self._path}/{identifier}")

    def _sub(
        self,
        identifier: str,
        sub: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.get(
            f"{self._path}/{identifier}/{sub}", params=params
        )

    def _post(
        self,
        path: str | None = None,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.post(
            path or self._path, json=json, params=params
        )

    def _patch(
        self,
        identifier: str,
        json: Any = None,
    ) -> Any:
        return self._http.patch(
            f"{self._path}/{identifier}", json=json
        )


class AsyncResource:
    """Base class for asynchronous resource clients."""

    _path: str

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def _list(
        self,
        params: dict[str, Any] | None = None,
        **extra: Any,
    ) -> PaginatedResponse:
        merged = {**(params or {}), **extra}
        merged = {k: v for k, v in merged.items() if v is not None}
        data = await self._http.get(self._path, params=merged)
        return _parse_paginated(data)

    async def _get(self, identifier: str) -> dict[str, Any]:
        return await self._http.get(f"{self._path}/{identifier}")

    async def _sub(
        self,
        identifier: str,
        sub: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self._http.get(
            f"{self._path}/{identifier}/{sub}", params=params
        )

    async def _post(
        self,
        path: str | None = None,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self._http.post(
            path or self._path, json=json, params=params
        )

    async def _patch(
        self,
        identifier: str,
        json: Any = None,
    ) -> Any:
        return await self._http.patch(
            f"{self._path}/{identifier}", json=json
        )


# -- helpers -----------------------------------------------------------


def _parse_paginated(data: Any) -> PaginatedResponse:
    """Parse a paginated API response into a PaginatedResponse."""
    if isinstance(data, dict):
        return PaginatedResponse(
            items=data.get("items", data.get("data", [])),
            total=data.get("total", 0),
            offset=data.get("offset", 0),
            limit=data.get("limit", 100),
        )
    if isinstance(data, list):
        return PaginatedResponse(
            items=data, total=len(data), offset=0, limit=len(data)
        )
    return PaginatedResponse()
