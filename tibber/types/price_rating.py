"""A class representing the PriceRating type from the GraphQL Tibber API."""


class PriceRating:
    """A class to get the rating of a price in relative terms."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def threshold_percentages(self) -> dict:
        # TODO: Create a PriceRatingThresholdPercentages type.
        return self.cache.get("thresholdPercentages")

    @property
    def hourly(self) -> dict:
        # TODO: Create a PriceRatingType type
        return self.cache.get("hourly")

    @property
    def daily(self) -> dict:
        # TODO: Create a PriceRatingType type
        return self.cache.get("daily")

    @property
    def monthly(self) -> dict:
        # TODO: Create a PriceRatingType type
        return self.cache.get("monthly")