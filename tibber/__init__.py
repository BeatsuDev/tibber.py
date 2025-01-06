__version__ = "0.5.0"
DEMO_TOKEN = "5K4MVS-OjfWhK_4yrjOlFe1F6kJXPVf7eQYggo8ebAE"
API_ENDPOINT = "https://api.tibber.com/v1-beta/gql"

import asyncio
import os

# The event loop type causes problems on windows systems when exiting.
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import modules after defining constants to avoid circular import error.
from .account import Account
from .types.home import NonDecoratedTibberHome, TibberHome

__all__ = [
    "__version__",
    "DEMO_TOKEN",
    "API_ENDPOINT",
    "Account",
    "NonDecoratedTibberHome",
    "TibberHome",
]
