"""A class representing the PriceInfo type from the GraphQL Tibber API."""
from tibber.types.price import Price

class PriceInfo:
    """A class to get price info."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def current(self) -> Price:
        """The energy price right now"""
        return Price(self.cache.get("current"), self.tibber_client)

    @property
    def today(self) -> list[Price]:
        """The hourly prices of the current day"""
        return [Price(hour, self.tibber_client) for hour in self.cache.get("today", [])]

    @property
    def tomorrow(self) -> list[Price]:
        """The hourly prices of the upcoming day"""
        return [Price(hour, self.tibber_client) for hour in self.cache.get("tomorrow", [])]
    
    # TODO: Implement range(resolution, first, last, ...) method