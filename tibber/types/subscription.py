"""A class representing the Subscription type from the GraphQL Tibber API."""
from tibber.types.legal_entity import LegalEntity
from tibber.types.price_info import PriceInfo
from tibber.types.price_rating import PriceRating


class Subscription:
    """A class to get information about the subscription of a TibberHome."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def id(self) -> str:
        return self.cache.get("id")

    @property
    def subscriber(self) -> LegalEntity:
        return LegalEntity(self.cache.get("subscriber"), self.tibber_client)

    @property
    def valid_from(self) -> str:
        return self.cache.get("validFrom")

    @property
    def valid_to(self) -> str:
        return self.cache.get("validTo")

    @property
    def status(self) -> str:
        return self.cache.get("status")

    @property
    def price_info(self) -> PriceInfo:
        return PriceInfo(self.cache.get("priceInfo"), self.tibber_client)

    @property
    def price_rating(self) -> PriceRating:
        return PriceRating(self.cache.get("priceRating"), self.tibber_client)