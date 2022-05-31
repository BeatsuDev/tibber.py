"""A class representing the ContactInfo type from the GraphQL Tibber API."""


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
        return self.cache.get("mobile")