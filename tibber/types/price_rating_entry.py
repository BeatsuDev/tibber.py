from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class PriceRatingEntry:
    """A dataclass representing the PriceRatingEntry type from the GraphQL Tibber API."""
    time: str = field(default=None)
    energy: float = field(default=None)
    total: float = field(default=None)
    tax: float = field(default=None)
    difference: float = field(default=None)
    level: str = field(default=None)
