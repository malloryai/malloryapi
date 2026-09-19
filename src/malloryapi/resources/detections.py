"""Detection packages, revisions, content manifests, and ZIP downloads."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import _parse_paginated
from malloryapi.resources.detection_signatures import (
    AsyncDetectionSignatures,
    DetectionSignatures,
)


class Detections(DetectionSignatures):
    _path = "/detections"

    def revisions(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> PaginatedResponse:
        data = self._sub(
            identifier, "revisions", params={"offset": offset, "limit": limit}
        )
        return _parse_paginated(data)

    def content(
        self,
        identifier: str,
        *,
        revision_uuid: str | None = None,
    ) -> dict[str, Any]:
        return self._sub(identifier, "content", params={"revision_uuid": revision_uuid})

    def download(
        self,
        identifier: str,
        *,
        revision_uuid: str | None = None,
    ) -> bytes:
        """Return the revision ZIP archive as bytes."""
        return self._http.get_bytes(
            f"{self._path}/{quote(identifier, safe='')}/download",
            params={"revision_uuid": revision_uuid},
        )


class AsyncDetections(AsyncDetectionSignatures):
    _path = "/detections"

    async def revisions(
        self,
        identifier: str,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> PaginatedResponse:
        data = await self._sub(
            identifier, "revisions", params={"offset": offset, "limit": limit}
        )
        return _parse_paginated(data)

    async def content(
        self,
        identifier: str,
        *,
        revision_uuid: str | None = None,
    ) -> dict[str, Any]:
        return await self._sub(
            identifier, "content", params={"revision_uuid": revision_uuid}
        )

    async def download(
        self,
        identifier: str,
        *,
        revision_uuid: str | None = None,
    ) -> bytes:
        """Return the revision ZIP archive as bytes."""
        return await self._http.get_bytes(
            f"{self._path}/{quote(identifier, safe='')}/download",
            params={"revision_uuid": revision_uuid},
        )
