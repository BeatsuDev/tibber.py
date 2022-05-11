"""A class representing the Production type from the GraphQL Tibber API."""


class Production:
    """A class containing concrete household electricity production information for a time period."""
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
    def production(self) -> float:
        return self.cache.get("production")

    @property
    def production_nit(self) -> str:
        return self.cache.get("productionUnit")

    @property
    def profit(self) -> float:
        return self.cache.get("profit")

    @property
    def currency(self) -> str:
        return self.cache.get("currency")