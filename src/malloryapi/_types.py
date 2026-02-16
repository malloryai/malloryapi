"""Shared types for the Mallory API client."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PaginatedResponse:
    """Response from a paginated list endpoint."""

    items: list[dict[str, Any]] = field(default_factory=list)
    total: int = 0
    offset: int = 0
    limit: int = 100

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    @property
    def has_more(self) -> bool:
        """Whether there are more pages available."""
        return self.offset + self.limit < self.total
