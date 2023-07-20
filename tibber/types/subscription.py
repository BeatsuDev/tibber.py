from __future__ import annotations

"""A class representing the Subscription type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.legal_entity import LegalEntity
from tibber.types.price_info import PriceInfo
from tibber.types.price_rating import PriceRating

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class Subscription:
    """A class to get information about the subscription of a TibberHome."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def id(self) -> str:
        return self.cache.get("id")

    @property
    def subscriber(self) -> LegalEntity:
        """The owner of the subscription"""
        return LegalEntity(self.cache.get("subscriber"), self.tibber_client)

    @property
    def valid_from(self) -> str:
        """The time the subscription started"""
        return self.cache.get("validFrom")

    @property
    def valid_to(self) -> str:
        """The time the subscription ended"""
        return self.cache.get("validTo")

    @property
    def status(self) -> str:
        """The current status of the subscription"""
        return self.cache.get("status")

    @property
    def price_info(self) -> PriceInfo:
        """Price information related to the subscription"""
        return PriceInfo(self.cache.get("priceInfo"), self.tibber_client)

    @property
    def price_rating(self) -> PriceRating:
        """Price information related to the subscription"""
        return PriceRating(self.cache.get("priceRating"), self.tibber_client)
