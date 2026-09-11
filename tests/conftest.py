"""Shared test fixtures."""

import inspect
from typing import Any

import httpx
import pytest

from malloryapi import AsyncMalloryApi, MalloryApi

TEST_API_KEY = "test-api-key-1234"
TEST_BASE_URL = "https://api.mallory.ai/v1"

_UNSET = object()


class SdkTestHarness:
    """Exercise a real SDK client through an in-memory HTTP transport."""

    def __init__(self, client_type):
        self.requests: list[httpx.Request] = []
        self._response: dict[str, Any] | None = None
        transport = httpx.MockTransport(self._handle_request)
        self.client = client_type(
            api_key=TEST_API_KEY,
            base_url=TEST_BASE_URL,
            transport=transport,
        )

    def respond(
        self,
        *,
        json: Any = _UNSET,
        content: Any = _UNSET,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        if self._response is not None:
            raise AssertionError("The previous sdk response was not consumed")
        if json is not _UNSET and content is not _UNSET:
            raise ValueError("Set either json or content, not both")
        self._response = {"status_code": status_code, "headers": headers}
        if content is not _UNSET:
            self._response["content"] = content
        elif json is None:
            self._response["content"] = b"null"
        elif json is not _UNSET:
            self._response["json"] = json

    def _handle_request(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self._response is None:
            raise AssertionError("Call sdk.respond() before making an SDK request")

        response = self._response
        self._response = None
        return httpx.Response(request=request, **response)

    async def call(self, fn, *args, **kwargs):
        result = fn(*args, **kwargs)
        if inspect.isawaitable(result):
            return await result
        return result

@pytest.fixture(params=[MalloryApi, AsyncMalloryApi], ids=["sync", "async"])
async def sdk(request):
    """Create either SDK client with a real, network-free HTTP stack."""
    harness = SdkTestHarness(request.param)
    try:
        yield harness
    finally:
        if isinstance(harness.client, AsyncMalloryApi):
            await harness.client.aclose()
        else:
            harness.client.close()
        assert harness._response is None, "The configured sdk response was not consumed"
