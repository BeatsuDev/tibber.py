"""A class representing the HomeFeatures type from the GraphQL Tibber API."""


class HomeFeatures:
    """A class to get information about the features of a TibberHome."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: Client = tibber_client

    @property
    def real_time_consumption_enabled(self) -> bool:
        return self.cache.get("realTimeConsumptionEnabled")