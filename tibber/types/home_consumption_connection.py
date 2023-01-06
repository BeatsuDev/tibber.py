from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.home_consumption_page_info import HomeConsumptionPageInfo
from tibber.types.consumption import Consumption
from tibber.types.home_consumption_edge import HomeConsumptionEdge

@dataclass
class HomeConsumptionConnection:
    """A dataclass representing the HomeConsumptionConnection type from the GraphQL Tibber API."""
    resolution: str | None = field(default=None)
    page_info: HomeConsumptionPageInfo | None = field(default=None)
    nodes: list | None = field(default=None)
    edges: list | None = field(default=None)

    def __iter__(self):
        return iter(self.nodes)
