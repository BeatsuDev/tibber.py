"""A class representing the MeteringPointData type from the GraphQL Tibber API."""


class MeteringPointData:
    """A MeteringPointData type to get information about the grid company, metering point ID and other information of a TibberHome."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def consumption_ean(self) -> str:
        return self.cache.get("consumptionEan")

    @property
    def grid_company(self) -> str:
        return self.cache.get("gridCompany")

    @property
    def grid_area_code(self) -> str:
        return self.cache.get("gridAreaCode")

    @property
    def price_area_code(self) -> str:
        return self.cache.get("priceAreaCode")

    @property
    def production_ean(self) -> str:
        return self.cache.get("productionEan")

    @property
    def energy_tax_type(self) -> str:
        return self.cache.get("energyTaxType")

    @property
    def vat_type(self) -> str:
        return self.cache.get("vatType")

    @property
    def estimated_annual_consumption(self) -> int:
        return self.cache.get("estimatedAnnualConsumption")
