from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class HomeProductionPageInfo:
    """A dataclass representing the HomeProductionPageInfo type from the GraphQL Tibber API."""
    resolution: str | None = field(default=None)
    end_cursor: str | None = field(default=None)
    has_next_page: bool | None = field(default=None)
    has_previous_page: bool | None = field(default=None)
    start_cursor: str | None = field(default=None)
    count: int | None = field(default=None)
    currency: str | None = field(default=None)
    total_profit: float | None = field(default=None)
    total_production: float | None = field(default=None)
    filtered: int | None = field(default=None)