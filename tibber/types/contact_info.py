from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ContactInfo:
    """A dataclass representing the ContactInfo type from the GraphQL Tibber API."""
    email: str | None = field(default=None)
    mobile: str | None = field(default=None)
