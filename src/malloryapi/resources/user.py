"""User resource – current authenticated user info."""

from __future__ import annotations

from typing import Any

from malloryapi.resources._base import AsyncResource, SyncResource


class User(SyncResource):
    _path = "/user"

    def me(self) -> dict[str, Any]:
        """Get the current authenticated user's information.

        Returns the user's UUID, email, first name, and last name.
        Requires a valid API key or Clerk token.
        """
        return self._http.get(self._path)


class AsyncUser(AsyncResource):
    _path = "/user"

    async def me(self) -> dict[str, Any]:
        """Get the current authenticated user's information.

        Returns the user's UUID, email, first name, and last name.
        Requires a valid API key or Clerk token.
        """
        return await self._http.get(self._path)
