"""Vulnerable technology product configuration sets resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import InferenceResponse, PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_inference,
)


class VulnerableConfigurations(SyncResource):
    _path = "/vulnerable_technology_product_configuration_sets"

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

    def get(self, identifier: str) -> dict[str, Any]:
        return self._get(identifier)

    def by_configuration(
        self, configuration_uuid: str
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/by-configuration/{quote(configuration_uuid, safe='')}"
        )

    def by_vulnerability(
        self, vulnerability_uuid: str
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/by-vulnerability/{quote(vulnerability_uuid, safe='')}"
        )

    def search(
        self, query: dict[str, Any], **kwargs: Any
    ) -> InferenceResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = self._http.post(
            f"{self._path}/search", json=query, params=params
        )
        return _parse_inference(data)


class AsyncVulnerableConfigurations(AsyncResource):
    _path = "/vulnerable_technology_product_configuration_sets"

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

    async def get(self, identifier: str) -> dict[str, Any]:
        return await self._get(identifier)

    async def by_configuration(
        self, configuration_uuid: str
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/by-configuration/{quote(configuration_uuid, safe='')}"
        )

    async def by_vulnerability(
        self, vulnerability_uuid: str
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/by-vulnerability/{quote(vulnerability_uuid, safe='')}"
        )

    async def search(
        self, query: dict[str, Any], **kwargs: Any
    ) -> InferenceResponse:
        params = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._http.post(
            f"{self._path}/search", json=query, params=params
        )
        return _parse_inference(data)


class Vtpcs(SyncResource):
    """Short-path resource for vulnerable configuration inference."""

    _path = "/vtpcs"

    def search(
        self, query: dict[str, Any], **kwargs: Any
    ) -> InferenceResponse:
        data = self._http.post(
            f"{self._path}/search", json=query, params=kwargs
        )
        return _parse_inference(data)


class AsyncVtpcs(AsyncResource):
    """Async short-path resource for vulnerable configuration inference."""

    _path = "/vtpcs"

    async def search(
        self, query: dict[str, Any], **kwargs: Any
    ) -> InferenceResponse:
        data = await self._http.post(
            f"{self._path}/search", json=query, params=kwargs
        )
        return _parse_inference(data)
