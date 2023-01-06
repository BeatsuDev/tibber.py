from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class PushNotificationResponse:
    """A dataclass representing the PushNotificationResponse type from the GraphQL Tibber API."""
    successful: bool = field(default=None)
    pushed_to_number_of_devices: int = field(default=None)
