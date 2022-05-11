"""A class representing the HomeProductionEdge type from the GraphQL Tibber API."""
from tibber.types.production import Production


class HomeProductionEdge:
    """A class containing household electricity production information for a time period."""
    def __init__(self, resolution: str, data: dict, tibber_client: "Client"):
        self.resolution = resolution
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def cursor(self) -> str:
        return self.cache.get("cursor")

    @property
    def node(self) -> Production:
        return Production(self.cache.get("node"), self.tibber_client)