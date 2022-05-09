"""A class representing the PriceRatingThresholdPercentages type from the GraphQL Tibber API."""


class PriceRatingThresholdPercentages:
    """A class to get price info."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def high(self) -> float:
        return self.cache.get("high")

    @property
    def low(self) -> float:
        return self.cache.get("current")