from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.consumption import Consumption


@dataclass
class HomeConsumptionEdge:
    """A dataclass representing the HomeConsumptionEdge type from the GraphQL Tibber API."""
    cursor: str | None = field(default=None)
    node: Consumption | None = field(default=None)
