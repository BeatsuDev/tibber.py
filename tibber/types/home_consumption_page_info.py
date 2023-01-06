from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class HomeConsumptionPageInfo:
    """A dataclass representing the HomeConsumptionPageInfo type from the GraphQL Tibber API."""
    end_cursor: str | None = field(default=None)
    has_next_page: bool | None = field(default=None)
    has_previous_page: bool | None = field(default=None)
    start_cursor: str | None = field(default=None)
    count: int | None = field(default=None)
    currency: str | None = field(default=None)
    total_cost: float | None = field(default=None)
    total_consumption: float | None = field(default=None)
    filtered: int | None = field(default=None)
