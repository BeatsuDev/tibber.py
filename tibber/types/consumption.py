from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Consumption:
    """A dataclass representing the Consumption type from the GraphQL Tibber API."""
    from_time: str | None = field(default=None)
    to_time: str | None = field(default=None)
    unit_price: float | None = field(default=None)
    unit_price_vat: float | None = field(default=None)
    consumption: float | None = field(default=None)
    consumption_unit: str | None = field(default=None)
    cost: float | None = field(default=None)
    currency: str | None = field(default=None)