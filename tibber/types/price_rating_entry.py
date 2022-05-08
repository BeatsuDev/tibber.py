"""A class representing the PriceRatingEntry type from the GraphQL Tibber API."""


class PriceRatingEntry:
    """A class to get the rating of a price in relative terms."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def time(self) -> str:
        return self.cache.get("time")

    @property
    def energy(self) -> float:
        return self.cache.get("energy")

    @property
    def total(self) -> float:
        return self.cache.get("total")

    @property
    def tax(self) -> float:
        return self.cache.get("tax")

    @property
    def difference(self) -> float:
        return self.cache.get("difference")

    @property
    def level(self) -> str:
        return self.cache.get("level")