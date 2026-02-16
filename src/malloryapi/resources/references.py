"""References resource."""

from __future__ import annotations

from typing import Any

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import AsyncResource, SyncResource


class References(SyncResource):
    _path = "/references"

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            **kwargs,
        )

    def labels(self) -> Any:
        return self._http.get(f"{self._path}/labels")

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def entities(self, identifier: str) -> Any:
        return self._sub(identifier, "entities")

    def create(self, urls: list[str]) -> Any:
        return self._post(json={"urls": urls})

    def threat_actors(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "threat-actors", params=kwargs
        )

    def threat_actor_mentions(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "threat-actor-mentions", params=kwargs
        )

    def vulnerabilities(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "vulnerabilities", params=kwargs
        )

    def vulnerability_mentions(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return self._sub(
            identifier, "vulnerability-mentions", params=kwargs
        )


class AsyncReferences(AsyncResource):
    _path = "/references"

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        sort: str | None = None,
        order: str | None = None,
        filter: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        return await self._list(
            offset=offset, limit=limit,
            sort=sort, order=order, filter=filter,
            **kwargs,
        )

    async def labels(self) -> Any:
        return await self._http.get(f"{self._path}/labels")

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def entities(self, identifier: str) -> Any:
        return await self._sub(identifier, "entities")

    async def create(self, urls: list[str]) -> Any:
        return await self._post(json={"urls": urls})

    async def threat_actors(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "threat-actors", params=kwargs
        )

    async def threat_actor_mentions(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "threat-actor-mentions", params=kwargs
        )

    async def vulnerabilities(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "vulnerabilities", params=kwargs
        )

    async def vulnerability_mentions(
        self, identifier: str, **kwargs: Any
    ) -> Any:
        return await self._sub(
            identifier, "vulnerability-mentions", params=kwargs
        )
