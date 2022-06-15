"""A class representing the ContactInfo type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.client import Client


class ContactInfo:
    """A class to get email and mobile. This info is probably of a LegalEntity."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data or {}
        self.tibber_client: "Client" = tibber_client

    @property
    def email(self) -> str:
        """The email of the corresponding entity"""
        return self.cache.get("email")

    @property
    def mobile(self) -> str:
        """The mobile phone no of the corresponding entity"""
        return self.cache.get("mobile")  # pragma: no cover