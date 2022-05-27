"""A class representing the PriceRating type from the GraphQL Tibber API."""
from tibber.types.price_rating_threshold_percentages import PriceRatingThresholdPercentages
from tibber.types.price_rating_type import PriceRatingType


class PriceRating:
    """A class to get the rating of a price in relative terms."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def threshold_percentages(self) -> dict:
        return PriceRatingThresholdPercentages(self.cache.get("thresholdPercentages"), self.tibber_client)

    @property
    def hourly(self) -> dict:
        return PriceRatingType(self.cache.get("hourly"), self.tibber_client)

    @property
    def daily(self) -> dict:
        return PriceRatingType(self.cache.get("daily"), self.tibber_client)

    @property
    def monthly(self) -> dict:
        return PriceRatingType(self.cache.get("monthly"), self.tibber_client)