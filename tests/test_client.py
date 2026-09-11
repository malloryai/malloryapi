"""Tests for client construction and configuration."""

import inspect

import httpx
import pytest

from malloryapi import AsyncMalloryApi, MalloryApi
from malloryapi.exceptions import AuthenticationError

CLIENT_TYPES = [MalloryApi, AsyncMalloryApi]


class CloseTrackingTransport(httpx.MockTransport):
    def __init__(self):
        super().__init__(lambda request: httpx.Response(200, request=request))
        self.closed = False

    def close(self):
        self.closed = True
        super().close()

    async def aclose(self):
        self.closed = True
        await super().aclose()


def _recording_transport(requests):
    def handle(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={"message": "OK", "status": "HEALTHY"},
            request=request,
        )

    return httpx.MockTransport(handle)


async def _call(fn, *args, **kwargs):
    result = fn(*args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    return result


async def _close(client):
    close = getattr(client, "aclose", None) or client.close
    await _call(close)


@pytest.mark.parametrize("client_type", CLIENT_TYPES, ids=["sync", "async"])
async def test_api_key_from_environment_reaches_request(
    client_type, monkeypatch
):
    monkeypatch.setenv("MALLORY_API_KEY", "environment-key")
    requests = []
    client = client_type(transport=_recording_transport(requests))
    try:
        await _call(client.health)
    finally:
        await _close(client)

    assert requests[0].headers["authorization"] == "Bearer environment-key"


@pytest.mark.parametrize("client_type", CLIENT_TYPES, ids=["sync", "async"])
async def test_explicit_configuration_reaches_request(client_type, monkeypatch):
    monkeypatch.setenv("MALLORY_API_KEY", "environment-key")
    requests = []
    client = client_type(
        api_key="explicit-key",
        base_url="https://proxy.example/custom/v1/",
        timeout=4.25,
        transport=_recording_transport(requests),
    )
    try:
        await _call(client.health)
    finally:
        await _close(client)

    request = requests[0]
    assert str(request.url) == "https://proxy.example/custom/v1/health"
    assert request.headers["authorization"] == "Bearer explicit-key"
    assert request.extensions["timeout"] == {
        "connect": 4.25,
        "read": 4.25,
        "write": 4.25,
        "pool": 4.25,
    }


@pytest.mark.parametrize("client_type", CLIENT_TYPES, ids=["sync", "async"])
def test_missing_api_key_fails_before_any_request(client_type, monkeypatch):
    monkeypatch.delenv("MALLORY_API_KEY", raising=False)
    requests = []

    with pytest.raises(AuthenticationError, match="No API key"):
        client_type(transport=_recording_transport(requests))

    assert requests == []


@pytest.mark.parametrize("client_type", CLIENT_TYPES, ids=["sync", "async"])
async def test_context_manager_closes_transport_on_exception(client_type):
    transport = CloseTrackingTransport()
    client = client_type(api_key="test-key", transport=transport)

    with pytest.raises(RuntimeError, match="application failure"):
        if isinstance(client, AsyncMalloryApi):
            async with client:
                raise RuntimeError("application failure")
        else:
            with client:
                raise RuntimeError("application failure")

    assert transport.closed is True
