from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Production:
    """A dataclass representing the Production type from the GraphQL Tibber API."""
    from_time: str = field(default=None)
    to_time: str = field(default=None)
    unit_price: float = field(default=None)
    unit_price_vat: float = field(default=None)
    production: float = field(default=None)
    production_unit: str = field(default=None)
    profit: float = field(default=None)
    currency: str = field(default=None)
