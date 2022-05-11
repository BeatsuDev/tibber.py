"""A class representing the HomeProductionPageInfo type from the GraphQL Tibber API."""


class HomeProductionPageInfo:
    """A class containing household electricity production information for a time period."""
    def __init__(self, resolution: str, data: dict, tibber_client: "Client"):
        self.resolution = resolution
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def end_cursor(self) -> str:
        return self.cache.get("endCursor")

    @property
    def has_next_page(self) -> bool:
        return self.cache.get("hasNextPage")

    @property
    def has_previous_page(self) -> bool:
        return self.cache.get("hasPreviousPage")

    @property
    def start_cursor(self) -> str:
        return self.cache.get("startCursor")

    @property
    def count(self) -> int:
        return self.cache.get("count")

    @property
    def currency(self) -> str:
        return self.cache.get("currency")

    @property
    def total_profit(self) -> float:
        return self.cache.get("totalProfit")

    @property
    def total_production(self) -> float:
        return self.cache.get("totalProduction")

    @property
    def filtered(self) -> int:
        return self.cache.get("filtered")