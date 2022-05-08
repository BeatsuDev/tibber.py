"""A class representing the PriceInfo type from the GraphQL Tibber API."""
from tibber.types.price import Price

class PriceInfo:
    """A class to get price info."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def current(self) -> Price:
        return Price(self.cache.get("current"), self.tibber_client)

    @property
    def today(self) -> list[Price]:
        return [Price(hour, self.tibber_client) for hour in self.cache.get("today")]

    @property
    def tomorrow(self) -> list[Price]:
        return [Price(hour, self.tibber_client) for hour in self.cache.get("tomorrow")]