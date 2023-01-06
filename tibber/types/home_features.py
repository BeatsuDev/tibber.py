from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class HomeFeatures:
    """A dataclass representing the HomeFeatures type from the GraphQL Tibber API."""
    real_time_consumption_enabled: bool | None = field(default=None)
