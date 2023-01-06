from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.home_production_page_info import HomeProductionPageInfo
from tibber.types.production import Production
from tibber.types.home_production_edge import HomeProductionEdge


@dataclass
class HomeProductionConnection:
    """A dataclass representing the HomeProductionConnection type from the GraphQL Tibber API."""
    resolution: str | None = field(default=None)
    page_info: HomeProductionPageInfo | None = field(default=None)
    nodes: list | None = field(default=None)
    edges: list | None = field(default=None)

    def __iter__(self):
        return iter(self.nodes)
