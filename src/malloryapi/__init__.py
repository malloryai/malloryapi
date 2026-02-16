"""malloryapi - Official Python client for the Mallory API."""

from malloryapi._pagination import paginate_async, paginate_sync
from malloryapi._types import PaginatedResponse
from malloryapi.client import AsyncMalloryApi, MalloryApi
from malloryapi.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

__all__ = [
    "MalloryApi",
    "AsyncMalloryApi",
    "PaginatedResponse",
    "paginate_sync",
    "paginate_async",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]

__version__ = "0.1.0"
