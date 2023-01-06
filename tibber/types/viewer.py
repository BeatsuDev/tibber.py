from __future__ import annotations
from dataclasses import dataclass, field

from tibber.types.home import Home


@dataclass
class Viewer:
    """A dataclass representing the Viewer type from the GraphQL Tibber API."""
    name: str = field(default=None)
    login: str = field(default=None)
    user_id: str = field(default=None)
    account_type: str = field(default=None)
    homes: list[Home] = field(default=None)
    websocket_subscription_url: str = field(default=None)
    
    # TODO: Implement home(id: ID!): Home! method. (get_home and fetch_home)
