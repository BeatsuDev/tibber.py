from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.production import Production


@dataclass
class HomeProductionEdge:
    """A dataclass representing the HomeProductionEdge type from the GraphQL Tibber API."""
    cursor: str | None = field(default=None)
    node: Production | None = field(default=None)
