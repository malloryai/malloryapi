"""Exceptions raised by the Mallory API client."""

from __future__ import annotations

from typing import Any


class APIError(Exception):
    """Base exception for all Mallory API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: Any = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class AuthenticationError(APIError):
    """Raised on 401 or 403 responses."""


class NotFoundError(APIError):
    """Raised on 404 responses."""


class ValidationError(APIError):
    """Raised on 422 responses."""


class RateLimitError(APIError):
    """Raised on 429 responses."""
