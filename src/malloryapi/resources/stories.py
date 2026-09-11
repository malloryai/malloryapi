"""Stories resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from malloryapi._types import PaginatedResponse
from malloryapi.resources._base import (
    AsyncResource,
    SyncResource,
    _parse_paginated,
)

_OMIT = object()


def _parse_story_observables(
    data: Any, *, offset: int, limit: int
) -> PaginatedResponse:
    """Adapt the story-specific observables envelope without dropping items."""
    if isinstance(data, dict) and "observables" in data:
        items = data.get("observables", [])
        total = data.get("total", len(items))
        return PaginatedResponse(
            items=items,
            total=total,
            offset=offset,
            limit=limit,
        )
    return _parse_paginated(data)


class Stories(SyncResource):
    _path = "/stories"

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
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            filter=filter,
            **kwargs,
        )

    def topics(
        self,
        *,
        sort: str = "story_count",
        order: str = "desc",
        story_count__gt: int | None = None,
        story_count__gte: int | None = None,
        story_count__lt: int | None = None,
        story_count__lte: int | None = None,
        latest_story_timestamp__gt: str | None = None,
        latest_story_timestamp__gte: str | None = None,
        latest_story_timestamp__lt: str | None = None,
        latest_story_timestamp__lte: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/topics",
            params={
                "sort": sort,
                "order": order,
                "story_count__gt": story_count__gt,
                "story_count__gte": story_count__gte,
                "story_count__lt": story_count__lt,
                "story_count__lte": story_count__lte,
                "latest_story_timestamp__gt": latest_story_timestamp__gt,
                "latest_story_timestamp__gte": latest_story_timestamp__gte,
                "latest_story_timestamp__lt": latest_story_timestamp__lt,
                "latest_story_timestamp__lte": latest_story_timestamp__lte,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )

    def topics_taxonomy(self) -> Any:
        return self._http.get(f"{self._path}/topics/taxonomy")

    def get(
        self,
        identifier: str,
        *,
        include_merged: bool = False,
        include_proto: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self._http.get(
            f"{self._path}/{quote(identifier, safe='')}",
            params={
                "include_merged": include_merged,
                "include_proto": include_proto,
                **kwargs,
            },
        )

    def references(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = self._sub(identifier, "references", params=kwargs)
        return _parse_paginated(data)

    def events(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = self._sub(identifier, "events", params=kwargs)
        return _parse_paginated(data)

    def similar(self, identifier: str, **kwargs: Any) -> list[dict[str, Any]]:
        return self._sub(identifier, "similar", params=kwargs)

    def entities(self, identifier: str, **kwargs: Any) -> Any:
        return self._sub(identifier, "entities", params=kwargs)

    def export(
        self,
        identifier: str,
        *,
        include_analysis: bool = True,
        relationships_created_after: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self._sub(
            identifier,
            "export",
            params={
                "include_analysis": include_analysis,
                "relationships_created_after": relationships_created_after,
                **kwargs,
            },
        )

    def update(
        self,
        identifier: str,
        *,
        title: Any = _OMIT,
        description: Any = _OMIT,
        reason: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        data = {}
        if title is not _OMIT:
            data["title"] = title
        if description is not _OMIT:
            data["description"] = description
        return self._patch(
            identifier,
            json=data,
            params={"reason": reason, **kwargs},
        )

    def citations(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = self._sub(identifier, "citations", params=kwargs)
        return _parse_paginated(data)

    def observables(
        self,
        identifier: str,
        *,
        observable_type: str | None = None,
        verdict: str | None = None,
        limit: int = 100,
        offset: int = 0,
        **kwargs: Any,
    ) -> PaginatedResponse:
        data = self._sub(
            identifier,
            "observables",
            params={
                "observable_type": observable_type,
                "verdict": verdict,
                "limit": limit,
                "offset": offset,
                **kwargs,
            },
        )
        return _parse_story_observables(data, offset=offset, limit=limit)

    def timeline(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = self._sub(identifier, "timeline", params=kwargs)
        return _parse_paginated(data)

    def exposure(
        self, identifier: str, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._sub(identifier, "exposure", params=params)
        return _parse_paginated(data)

    def delete(self, identifier: str) -> Any:
        return self._delete(identifier)


class AsyncStories(AsyncResource):
    _path = "/stories"

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
            offset=offset,
            limit=limit,
            sort=sort,
            order=order,
            filter=filter,
            **kwargs,
        )

    async def topics(
        self,
        *,
        sort: str = "story_count",
        order: str = "desc",
        story_count__gt: int | None = None,
        story_count__gte: int | None = None,
        story_count__lt: int | None = None,
        story_count__lte: int | None = None,
        latest_story_timestamp__gt: str | None = None,
        latest_story_timestamp__gte: str | None = None,
        latest_story_timestamp__lt: str | None = None,
        latest_story_timestamp__lte: str | None = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/topics",
            params={
                "sort": sort,
                "order": order,
                "story_count__gt": story_count__gt,
                "story_count__gte": story_count__gte,
                "story_count__lt": story_count__lt,
                "story_count__lte": story_count__lte,
                "latest_story_timestamp__gt": latest_story_timestamp__gt,
                "latest_story_timestamp__gte": latest_story_timestamp__gte,
                "latest_story_timestamp__lt": latest_story_timestamp__lt,
                "latest_story_timestamp__lte": latest_story_timestamp__lte,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )

    async def topics_taxonomy(self) -> Any:
        return await self._http.get(f"{self._path}/topics/taxonomy")

    async def get(
        self,
        identifier: str,
        *,
        include_merged: bool = False,
        include_proto: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._path}/{quote(identifier, safe='')}",
            params={
                "include_merged": include_merged,
                "include_proto": include_proto,
                **kwargs,
            },
        )

    async def references(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = await self._sub(identifier, "references", params=kwargs)
        return _parse_paginated(data)

    async def events(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = await self._sub(identifier, "events", params=kwargs)
        return _parse_paginated(data)

    async def similar(self, identifier: str, **kwargs: Any) -> list[dict[str, Any]]:
        return await self._sub(identifier, "similar", params=kwargs)

    async def entities(self, identifier: str, **kwargs: Any) -> Any:
        return await self._sub(identifier, "entities", params=kwargs)

    async def export(
        self,
        identifier: str,
        *,
        include_analysis: bool = True,
        relationships_created_after: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self._sub(
            identifier,
            "export",
            params={
                "include_analysis": include_analysis,
                "relationships_created_after": relationships_created_after,
                **kwargs,
            },
        )

    async def update(
        self,
        identifier: str,
        *,
        title: Any = _OMIT,
        description: Any = _OMIT,
        reason: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        data = {}
        if title is not _OMIT:
            data["title"] = title
        if description is not _OMIT:
            data["description"] = description
        return await self._patch(
            identifier,
            json=data,
            params={"reason": reason, **kwargs},
        )

    async def citations(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = await self._sub(identifier, "citations", params=kwargs)
        return _parse_paginated(data)

    async def observables(
        self,
        identifier: str,
        *,
        observable_type: str | None = None,
        verdict: str | None = None,
        limit: int = 100,
        offset: int = 0,
        **kwargs: Any,
    ) -> PaginatedResponse:
        data = await self._sub(
            identifier,
            "observables",
            params={
                "observable_type": observable_type,
                "verdict": verdict,
                "limit": limit,
                "offset": offset,
                **kwargs,
            },
        )
        return _parse_story_observables(data, offset=offset, limit=limit)

    async def timeline(self, identifier: str, **kwargs: Any) -> PaginatedResponse:
        data = await self._sub(identifier, "timeline", params=kwargs)
        return _parse_paginated(data)

    async def exposure(
        self, identifier: str, *, offset: int = 0, limit: int = 50, **kwargs: Any
    ) -> PaginatedResponse:
        params = {"offset": offset, "limit": limit, **kwargs}
        params = {k: v for k, v in params.items() if v is not None}
        data = await self._sub(identifier, "exposure", params=params)
        return _parse_paginated(data)

    async def delete(self, identifier: str) -> Any:
        return await self._delete(identifier)
