"""A class representing the Address type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.client import Client


class Address:
    """An address type to get information about the location of a TibberHome."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data or {}
        self.tibber_client: "Client" = tibber_client

    @property
    def address1(self) -> str:
        return self.cache.get("address1")

    @property
    def address2(self) -> str:
        return self.cache.get("address2")

    @property
    def address3(self) -> str:
        return self.cache.get("address3")

    @property
    def city(self) -> str:
        return self.cache.get("city")

    @property
    def postal_code(self) -> str:
        return self.cache.get("postalCode")

    @property
    def country(self) -> str:
        return self.cache.get("country")

    @property
    def latitude(self) -> str:
        return self.cache.get("latitude")

    @property
    def longitude(self) -> str:
        return self.cache.get("longitude")