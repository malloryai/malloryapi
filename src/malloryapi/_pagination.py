"""Auto-pagination iterators for sync and async usage."""

from __future__ import annotations

from typing import Any, AsyncIterator, Callable, Iterator


def paginate_sync(
    fetch: Callable[..., Any],
    limit: int = 100,
    **kwargs: Any,
) -> Iterator[dict[str, Any]]:
    """Yield all items across pages synchronously.

    Usage::

        for vuln in paginate_sync(client.vulnerabilities.list, limit=50):
            print(vuln["cve_id"])
    """
    offset = 0
    while True:
        page = fetch(offset=offset, limit=limit, **kwargs)
        items = page.items if hasattr(page, "items") else page
        if not items:
            break
        yield from items
        offset += limit
        if not page.has_more:
            break


async def paginate_async(
    fetch: Callable[..., Any],
    limit: int = 100,
    **kwargs: Any,
) -> AsyncIterator[dict[str, Any]]:
    """Yield all items across pages asynchronously.

    Usage::

        async for vuln in paginate_async(
            client.vulnerabilities.list, limit=50
        ):
            print(vuln["cve_id"])
    """
    offset = 0
    while True:
        page = await fetch(offset=offset, limit=limit, **kwargs)
        items = page.items if hasattr(page, "items") else page
        if not items:
            break
        for item in items:
            yield item
        offset += limit
        if not page.has_more:
            break
