"""A class representing the HomeConsumptionEdge type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.consumption import Consumption

# Import type checking modules
if TYPE_CHECKING:
    from tibber.client import Client


class HomeConsumptionEdge:
    """A class containing household electricity consumption information for a time period."""
    def __init__(self, resolution: str, data: dict, tibber_client: "Client"):
        self.resolution = resolution
        self.cache: dict = data or {}
        self.tibber_client: "Client" = tibber_client

    @property
    def cursor(self) -> str:
        return self.cache.get("cursor")

    @property
    def node(self) -> Consumption:
        return Consumption(self.cache.get("node"), self.tibber_client)