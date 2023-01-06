from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.price_rating_entry import PriceRatingEntry


@dataclass
class PriceRatingType:
    """A dataclass representing the PriceRatingType type from the GraphQL Tibber API."""
    min_energy: float = field(default=None)
    max_energy: float = field(default=None)
    min_total: float = field(default=None)
    max_total: float = field(default=None)
    currency: str = field(default=None)
    entries: list[PriceRatingEntry] = field(default_factory=list)
