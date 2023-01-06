from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.price import Price


@dataclass
class PriceInfo:
    """A dataclass representing the PriceInfo type from the GraphQL Tibber API."""
    current: Price = field(default=None)
    today: list[Price] = field(default_factory=list)
    tomorrow: list[Price] = field(default_factory=list)
    
    # TODO: Implement range(resolution, first, last, ...) method
