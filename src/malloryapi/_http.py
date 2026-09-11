"""HTTP client wrapper for sync and async requests."""

from __future__ import annotations

import os
from typing import Any

import httpx

from malloryapi.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

DEFAULT_BASE_URL = "https://api.mallory.ai/v1"
DEFAULT_TIMEOUT = 30.0


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get("MALLORY_API_KEY")
    if not key:
        raise AuthenticationError(
            "No API key provided. Pass api_key= or set the "
            "MALLORY_API_KEY environment variable."
        )
    return key


def _build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Drop absent query values while preserving falsey, meaningful values."""
    if params is None:
        return None
    return {key: value for key, value in params.items() if value is not None}


def _decode_success_response(response: httpx.Response) -> Any:
    """Decode a successful response, including documented empty successes."""
    if response.status_code == 204:
        return None
    return response.json()


def _handle_error_response(response: httpx.Response) -> None:
    """Raise the appropriate exception for non-2xx responses."""
    status = response.status_code
    try:
        body = response.json()
    except Exception:
        body = response.text

    if status in (401, 403):
        raise AuthenticationError(
            f"Authentication failed ({status})",
            status_code=status,
            response_body=body,
        )
    if status == 404:
        raise NotFoundError(
            "Resource not found",
            status_code=status,
            response_body=body,
        )
    if status == 422:
        raise ValidationError(
            f"Validation error: {body}",
            status_code=status,
            response_body=body,
        )
    if status == 429:
        raise RateLimitError(
            "Rate limit exceeded",
            status_code=status,
            response_body=body,
        )
    raise APIError(
        f"API request failed ({status})",
        status_code=status,
        response_body=body,
    )


def _decode_response(response: httpx.Response) -> Any:
    if response.status_code >= 400:
        _handle_error_response(response)
    return _decode_success_response(response)


class SyncHttpClient:
    """Synchronous HTTP client backed by httpx."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        resolved_key = _resolve_api_key(api_key)
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=_build_headers(resolved_key),
            timeout=timeout,
            transport=transport,
        )

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.get(path, params=_clean_params(params))
        return _decode_response(response)

    def post(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.post(path, json=json, params=_clean_params(params))
        return _decode_response(response)

    def put(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.put(path, json=json, params=_clean_params(params))
        return _decode_response(response)

    def patch(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.patch(path, json=json, params=_clean_params(params))
        return _decode_response(response)

    def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.delete(path, params=_clean_params(params))
        return _decode_response(response)

    def close(self) -> None:
        self._client.close()


class AsyncHttpClient:
    """Asynchronous HTTP client backed by httpx."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        resolved_key = _resolve_api_key(api_key)
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=_build_headers(resolved_key),
            timeout=timeout,
            transport=transport,
        )

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.get(path, params=_clean_params(params))
        return _decode_response(response)

    async def post(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.post(
            path, json=json, params=_clean_params(params)
        )
        return _decode_response(response)

    async def put(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.put(
            path, json=json, params=_clean_params(params)
        )
        return _decode_response(response)

    async def patch(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.patch(
            path, json=json, params=_clean_params(params)
        )
        return _decode_response(response)

    async def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.delete(path, params=_clean_params(params))
        return _decode_response(response)

    async def aclose(self) -> None:
        await self._client.aclose()
