"""A class representing the Consumption type from the GraphQL Tibber API."""


class Consumption:
    """A class containing concrete household electricity consumption information for a time period."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def from_time(self) -> str:
        return self.cache.get("from")

    @property
    def to_time(self) -> str:
        return self.cache.get("to")

    @property
    def unit_price(self) -> float:
        return self.cache.get("unitPrice")

    @property
    def unit_price_vat(self) -> float:
        return self.cache.get("unitPriceVAT")

    @property
    def consumption(self) -> float:
        """kWh consumed"""
        return self.cache.get("consumption")

    @property
    def consumption_unit(self) -> str:
        return self.cache.get("consumptionUnit")

    @property
    def cost(self) -> float:
        return self.cache.get("cost")

    @property
    def currency(self) -> str:
        """The cost currency"""
        return self.cache.get("currency")