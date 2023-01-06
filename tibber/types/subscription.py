from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.legal_entity import LegalEntity
from tibber.types.price_info import PriceInfo
from tibber.types.price_rating import PriceRating


@dataclass
class Subscription:
    """A dataclass representing the Subscription type from the GraphQL Tibber API."""
    id: str = field(default=None)
    subscriber: LegalEntity = field(default=None)
    valid_from: str = field(default=None)
    valid_to: str = field(default=None)
    status: str = field(default=None)
    price_info: PriceInfo = field(default=None)
    price_rating: PriceRating = field(default=None)
