from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class PriceRatingThresholdPercentages:
    """A dataclass representing the PriceRatingThresholdPercentages type from the GraphQL Tibber API."""
    high: float = field(default=None)
    low: float = field(default=None)
