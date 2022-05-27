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
        """The different 'high'/'low' price breakpoints (market dependent)"""
        return PriceRatingThresholdPercentages(self.cache.get("thresholdPercentages"), self.tibber_client)

    @property
    def hourly(self) -> dict:
        """The hourly prices of today, the previous 7 days, and tomorrow"""
        return PriceRatingType(self.cache.get("hourly"), self.tibber_client)

    @property
    def daily(self) -> dict:
        """The daily prices of today and the previous 30 days"""
        return PriceRatingType(self.cache.get("daily"), self.tibber_client)

    @property
    def monthly(self) -> dict:
        """The monthly prices of this month and the previous 31 months"""
        return PriceRatingType(self.cache.get("monthly"), self.tibber_client)