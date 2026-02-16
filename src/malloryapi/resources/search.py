"""Search resource."""

from __future__ import annotations

from typing import Any

from malloryapi._http import AsyncHttpClient, SyncHttpClient


class Search:
    """Synchronous search across entities."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def query(self, q: str, **kwargs: Any) -> Any:
        """Search across all entity types.

        Args:
            q: Search query string.
            **kwargs: Additional query parameters.
        """
        return self._http.get(
            "/search", params={"q": q, **kwargs}
        )


class AsyncSearch:
    """Asynchronous search across entities."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def query(self, q: str, **kwargs: Any) -> Any:
        """Search across all entity types.

        Args:
            q: Search query string.
            **kwargs: Additional query parameters.
        """
        return await self._http.get(
            "/search", params={"q": q, **kwargs}
        )
