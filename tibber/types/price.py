"""A class representing the Price type from the GraphQL Tibber API."""


class Price:
    """A class to get price info."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def total(self) -> float:
        return self.cache.get("total")

    @property
    def energy(self) -> float:
        return self.cache.get("energy")

    @property
    def tax(self) -> float:
        return self.cache.get("tax")

    @property
    def starts_at(self) -> str:
        return self.cache.get("startsAt")

    @property
    def currency(self) -> str:
        return self.cache.get("currency")

    @property
    def level(self) -> str:
        return self.cache.get("level")