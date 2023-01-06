from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Address:
    """A dataclass representing the Address type from the GraphQL Tibber API."""
    address1: str
    address2: str | None = field(default=None)
    address3: str | None = field(default=None)
    city: str | None = field(default=None)
    postal_code: str | None = field(default=None)
    country: str | None = field(default=None)
    latitude: str | None = field(default=None)
    longitude: str | None = field(default=None)
