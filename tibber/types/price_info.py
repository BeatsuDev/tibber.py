"""A class representing the PriceInfo type from the GraphQL Tibber API."""


class PriceInfo:
    """A class to get price info."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def current(self) -> dict:
        # TODO: Create a Price type
        return self.cache.get("current")

    @property
    def today(self) -> dict:
        # TODO: Create a Price type
        return self.cache.get("today")

    @property
    def tomorrow(self) -> dict:
        # TODO: Create a Price type
        return self.cache.get("tomorrow")