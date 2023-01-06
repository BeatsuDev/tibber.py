from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class MeteringPointData:
    """A class representing the MeteringPointData type from the GraphQL Tibber API."""
    consumption_ean: str = field(default=None)
    grid_company: str = field(default=None)
    grid_area_code: str = field(default=None)
    price_area_code: str = field(default=None)
    production_ean: str = field(default=None)
    energy_tax_type: str = field(default=None)
    vat_type: str = field(default=None)
    estimated_annual_consumption: int = field(default=None)
