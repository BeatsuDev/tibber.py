"""A class representing the PriceRatingType type from the GraphQL Tibber API."""
from tibber.types.price_rating_entry import PriceRatingEntry


class PriceRatingType:
    """A class to get the rating of a price in relative terms."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def min_energy(self) -> float:
        return self.cache.get("minEnergy")

    @property
    def max_energy(self) -> float:
        return self.cache.get("maxEnergy")

    @property
    def min_total(self) -> float:
        return self.cache.get("minTotal")

    @property
    def max_total(self) -> float:
        return self.cache.get("maxTotal")

    @property
    def currency(self) -> str:
        return self.cache.get("currency")

    @property
    def entries(self) -> list[PriceRatingEntry]:
        return [PriceRatingEntry(entry, self.tibber_client) for entry in self.cache.get("entries", [])]