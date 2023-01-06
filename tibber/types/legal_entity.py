from __future__ import annotations
from dataclasses import dataclass, field

from apischema.graphql import resolver

from tibber.types.contact_info import ContactInfo
from tibber.types.address import Address

@dataclass
class LegalEntity:
    """A dataclass representing the LegalEntity type from the GraphQL Tibber API."""
    id: str = field(default=None)
    first_name: str = field(default=None)
    is_company: bool = field(default=None)
    name: str = field(default=None)
    middle_name: str = field(default=None)
    last_name: str = field(default=None)
    organization_no: str = field(default=None)
    language: str = field(default=None)
    contact_info: ContactInfo = field(default=None)
    address: Address = field(default=None)