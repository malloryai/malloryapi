"""Shared test fixtures."""

import pytest

from malloryapi import AsyncMalloryApi, MalloryApi

TEST_API_KEY = "test-api-key-1234"
TEST_BASE_URL = "https://api.mallory.ai/v1"


@pytest.fixture
def client():
    """Create a sync MalloryApi client for testing."""
    c = MalloryApi(api_key=TEST_API_KEY)
    yield c
    c.close()


@pytest.fixture
async def async_client():
    """Create an async MalloryApi client for testing."""
    c = AsyncMalloryApi(api_key=TEST_API_KEY)
    yield c
    await c.aclose()
