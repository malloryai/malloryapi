"""Base resource classes for sync and async API access."""

from __future__ import annotations

from typing import Any, Literal
from urllib.parse import quote

from malloryapi._http import AsyncHttpClient, SyncHttpClient
from malloryapi._types import InferenceResponse, PaginatedResponse

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
        return self._http.get(f"{self._path}/{quote(identifier, safe='')}")

    def _sub(
        self,
        identifier: str,
        sub: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.get(
            f"{self._path}/{quote(identifier, safe='')}/{sub}", params=params
        )

    def _post(
        self,
        path: str | None = None,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.post(path or self._path, json=json, params=params)

    def _patch(
        self,
        identifier: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.patch(
            f"{self._path}/{quote(identifier, safe='')}", json=json, params=params
        )

    def _put(
        self,
        identifier: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self._http.put(
            f"{self._path}/{quote(identifier, safe='')}", json=json, params=params
        )

    def _delete(self, identifier: str) -> Any:
        return self._http.delete(f"{self._path}/{quote(identifier, safe='')}")


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
        return await self._http.get(f"{self._path}/{quote(identifier, safe='')}")

    async def _sub(
        self,
        identifier: str,
        sub: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self._http.get(
            f"{self._path}/{quote(identifier, safe='')}/{sub}", params=params
        )

    async def _post(
        self,
        path: str | None = None,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self._http.post(path or self._path, json=json, params=params)

    async def _patch(
        self,
        identifier: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self._http.patch(
            f"{self._path}/{quote(identifier, safe='')}", json=json, params=params
        )

    async def _put(
        self,
        identifier: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self._http.put(
            f"{self._path}/{quote(identifier, safe='')}", json=json, params=params
        )

    async def _delete(self, identifier: str) -> Any:
        return await self._http.delete(f"{self._path}/{quote(identifier, safe='')}")


# -- helpers -----------------------------------------------------------


def _parse_paginated(
    data: Any,
    *,
    items_key: str | None = None,
    total_key: str | None = None,
    is_paginated: bool = True,
) -> PaginatedResponse:
    """Parse a paginated API response into a PaginatedResponse."""
    if isinstance(data, dict):
        resolved_items_key = items_key
        if resolved_items_key is None:
            resolved_items_key = "items" if "items" in data else "data"
        items = data.get(resolved_items_key, [])
        resolved_total_key = total_key or "total"
        total = data.get(resolved_total_key)
        if total is None:
            total = len(items)
        metadata = {
            key: value
            for key, value in data.items()
            if key
            not in {
                resolved_items_key,
                "items",
                "data",
                "total",
                "offset",
                "limit",
            }
        }
        limit = data.get("limit", 100) if is_paginated else total
        return PaginatedResponse(
            items=items,
            total=total,
            offset=data.get("offset", 0),
            limit=limit,
            metadata=metadata,
        )
    if isinstance(data, list):
        return PaginatedResponse(items=data, total=len(data), offset=0, limit=len(data))
    return PaginatedResponse()


def _parse_inference(data: Any) -> InferenceResponse:
    """Parse an inference envelope without discarding resolution metadata."""
    parsed = _parse_paginated(data)
    if not isinstance(data, dict):
        return InferenceResponse(
            items=parsed.items,
            total=parsed.total,
            offset=parsed.offset,
            limit=parsed.limit,
            metadata=parsed.metadata,
        )
    return InferenceResponse(
        items=parsed.items,
        total=parsed.total,
        offset=parsed.offset,
        limit=parsed.limit,
        metadata=parsed.metadata,
        resolution=data.get("resolution"),
        normalized_request=data.get("normalized_request"),
        mode=data.get("mode"),
        coverage=data.get("coverage"),
    )
