"""A class representing the HomeConsumptionConnection type from the GraphQL Tibber API."""
from tibber.types.home_consumption_page_info import HomeConsumptionPageInfo
from tibber.types.consumption import Consumption
from tibber.types.home_consumption_edge import HomeConsumptionEdge


class HomeConsumptionConnection:
    """A class containing household electricity consumption information for a time period."""
    def __init__(self, resolution: str, data: dict, tibber_client: "Client"):
        self.resolution = resolution
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def page_info(self) -> str:
        return HomeConsumptionPageInfo(self.resolution, self.cache.get("pageInfo"), self.tibber_client)

    @property
    def nodes(self) -> list:
        return [Consumption(node, self.tibber_client) for node in self.cache.get("nodes")]

    @property
    def edges(self) -> list:
        return [HomeConsumptionEdge(self.resolution, edge, self.tibber_client) for edge in self.cache.get("edges")]