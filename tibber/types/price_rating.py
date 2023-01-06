from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.price_rating_threshold_percentages import PriceRatingThresholdPercentages
from tibber.types.price_rating_type import PriceRatingType


@dataclass
class PriceRating:
    """A dataclass representing the PriceRating type from the GraphQL Tibber API."""
    threshold_percentages: PriceRatingThresholdPercentages = field(default=None)
    hourly: PriceRatingType = field(default=None)
    daily: PriceRatingType = field(default=None)
    monthly: PriceRatingType = field(default=None)
