"""Integration deletion preserves an explicitly selected force value."""

import pytest


@pytest.mark.parametrize("force", [False, True])
async def test_delete_forwards_force(sdk, force):
    sdk.respond(status_code=204)

    result = await sdk.call(
        sdk.client.integrations.delete, "integration-id", force=force
    )

    assert result is None
    assert sdk.requests[0].url.params["force"] == str(force).lower()
