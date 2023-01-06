from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Price:
    """A dataclass representing the Price type from the GraphQL Tibber API."""
    total: float = field(default=None)
    energy: float = field(default=None)
    tax: float = field(default=None)
    starts_at: str = field(default=None)
    currency: str = field(default=None)
    level: str = field(default=None)
