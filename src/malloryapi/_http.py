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


class SyncHttpClient:
    """Synchronous HTTP client backed by httpx."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        resolved_key = _resolve_api_key(api_key)
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=_build_headers(resolved_key),
            timeout=timeout,
        )

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.get(path, params=params)
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    def post(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.post(path, json=json, params=params)
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    def patch(
        self,
        path: str,
        json: Any = None,
    ) -> Any:
        response = self._client.patch(path, json=json)
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._client.delete(path, params=params)
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    def close(self) -> None:
        self._client.close()


class AsyncHttpClient:
    """Asynchronous HTTP client backed by httpx."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        resolved_key = _resolve_api_key(api_key)
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=_build_headers(resolved_key),
            timeout=timeout,
        )

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.get(path, params=params)
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    async def post(
        self,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.post(
            path, json=json, params=params
        )
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    async def patch(
        self,
        path: str,
        json: Any = None,
    ) -> Any:
        response = await self._client.patch(path, json=json)
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    async def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.delete(path, params=params)
        if response.status_code >= 400:
            _handle_error_response(response)
        return response.json()

    async def aclose(self) -> None:
        await self._client.aclose()
