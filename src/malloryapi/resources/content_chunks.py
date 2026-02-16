"""Content chunks resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import AsyncResource, SyncResource


class ContentChunks(SyncResource):
    _path = "/content_chunks"

    def list(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        return self._list(offset=offset, limit=limit, **kwargs)

    def search(self, **kwargs: Any) -> PaginatedResponse:
        from malloryapi.resources._base import _parse_paginated
        data = self._http.get(
            f"{self._path}/search", params=kwargs
        )
        return _parse_paginated(data)

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)


class AsyncContentChunks(AsyncResource):
    _path = "/content_chunks"

    async def list(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit, **kwargs
        )

    async def search(self, **kwargs: Any) -> PaginatedResponse:
        from malloryapi.resources._base import _parse_paginated
        data = await self._http.get(
            f"{self._path}/search", params=kwargs
        )
        return _parse_paginated(data)

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)
