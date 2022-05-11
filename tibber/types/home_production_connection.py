"""A class representing the HomeProductionConnection type from the GraphQL Tibber API."""
from tibber.types.home_production_page_info import HomeProductionPageInfo
from tibber.types.production import Production


class HomeProductionConnection:
    """A class containing household electricity production information for a time period."""
    def __init__(self, resolution: str, data: dict, tibber_client: "Client"):
        self.resolution = resolution
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def page_info(self) -> str:
        return HomeProductionPageInfo(self.resolution, self.cache.get("pageInfo"), self.tibber_client)

    @property
    def nodes(self) -> list:
        return [Production(node, self.tibber_client) for node in self.cache.get("nodes")]

    @property
    def edges(self) -> list:
        return self.cache.get("edges")