__version__ = "0.0.1"
DEMO_TOKEN = "476c477d8a039529478ebd690d35ddd80e3308ffc49b59c65b142321aee963a4"
API_ENDPOINT = "https://api.tibber.com/v1-beta/gql"
SUBSCRIPTION_ENDPOINT = "wss://api.tibber.com/v1-beta/gql/subscriptions"

# Import modules after definig constants to avoid circular import error.
from tibber.enums import Resolution
from tibber.client import Client

from tibber.types.address import Address
from tibber.types.legal_entity import LegalEntity
from tibber.types.price_info import PriceInfo
from tibber.types.price_rating import PriceRating
from tibber.types.metering_point_data import MeteringPointData
from tibber.types.subscription import Subscription
from tibber.types.home import TibberHome
from tibber.types.home import DecoratedTibberHome