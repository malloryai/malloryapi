"""Mentions resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)


class Mentions(SyncResource):
    _path = "/mentions"

    def list(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        return self._list(offset=offset, limit=limit, **kwargs)

    def actors(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        data = self._http.get(
            f"{self._path}/actors",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        return _parse_paginated(data)

    def vulnerabilities(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        data = self._http.get(
            f"{self._path}/vulnerabilities",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        return _parse_paginated(data)


class AsyncMentions(AsyncResource):
    _path = "/mentions"

    async def list(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit, **kwargs
        )

    async def actors(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        data = await self._http.get(
            f"{self._path}/actors",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        return _parse_paginated(data)

    async def vulnerabilities(
        self, *, offset: int = 0, limit: int = 100, **kwargs: Any
    ) -> PaginatedResponse:
        data = await self._http.get(
            f"{self._path}/vulnerabilities",
            params={"offset": offset, "limit": limit, **kwargs},
        )
        return _parse_paginated(data)
