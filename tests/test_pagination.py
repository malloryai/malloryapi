"""Auto-pagination behavior using its existing fetch dependency."""

import pytest

from malloryapi import PaginatedResponse, paginate_async, paginate_sync


@pytest.fixture(params=["sync", "async"])
def collect_pages(request):
    async def collect(fetch, **kwargs):
        if request.param == "sync":
            return list(paginate_sync(fetch, **kwargs))

        async def async_fetch(**params):
            return fetch(**params)

        return [item async for item in paginate_async(async_fetch, **kwargs)]

    return collect


async def test_advances_offsets_and_preserves_filters(collect_pages):
    calls = []

    def fetch(**params):
        calls.append(params)
        offset = params["offset"]
        return PaginatedResponse(
            items=[{"id": i} for i in range(offset, min(offset + 2, 3))],
            total=3, offset=offset, limit=2,
        )

    assert await collect_pages(fetch, limit=2, filter="active") == [
        {"id": 0}, {"id": 1}, {"id": 2},
    ]
    assert calls == [
        {"offset": 0, "limit": 2, "filter": "active"},
        {"offset": 2, "limit": 2, "filter": "active"},
    ]


async def test_stops_on_empty_page_even_when_total_indicates_more(collect_pages):
    calls = []

    def fetch(**params):
        calls.append(params)
        assert len(calls) == 1, "An empty page must terminate pagination"
        return PaginatedResponse(items=[], total=1000, offset=0, limit=10)

    assert await collect_pages(fetch, limit=10) == []
    assert len(calls) == 1


async def test_propagates_fetch_errors(collect_pages):
    error = RuntimeError("page request failed")

    def fetch(**params):
        raise error

    with pytest.raises(RuntimeError) as caught:
        await collect_pages(fetch)
    assert caught.value is error


@pytest.mark.parametrize("limit", [0, -1])
async def test_rejects_nonpositive_limit_before_fetch(collect_pages, limit):
    def fetch(**params):
        pytest.fail("Invalid page sizes must not make a request")

    with pytest.raises(ValueError, match="positive"):
        await collect_pages(fetch, limit=limit)
