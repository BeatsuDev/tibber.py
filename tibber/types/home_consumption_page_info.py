"""A class representing the HomeConsumptionPageInfo type from the GraphQL Tibber API."""


class HomeConsumptionPageInfo:
    """A class containing household electricity consumption information for a time period."""
    def __init__(self, resolution: str, data: dict, tibber_client: "Client"):
        self.resolution = resolution
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def endCursor(self) -> str:
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
    def total_cost(self) -> float:
        return self.cache.get("totalCost")

    @property
    def total_consumption(self) -> float:
        return self.cache.get("totalConsumption")

    @property
    def filtered(self) -> int:
        return self.cache.get("filtered")