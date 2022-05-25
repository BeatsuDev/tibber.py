"""Classes representing the Home type from the GraphQL Tibber API."""
import asyncio
import websockets
from typing import Callable

from tibber import SUBSCRIPTION_ENDPOINT
from tibber.types.legal_entity import LegalEntity
from tibber.types.address import Address
from tibber.types.metering_point_data import MeteringPointData
from tibber.types.subscription import Subscription
from tibber.types.home_features import HomeFeatures
from tibber.types.home_consumption_connection import HomeConsumptionConnection
from tibber.types.home_production_connection import HomeProductionConnection
from tibber.networking import QueryBuilder


class NonDecoratedTibberHome:
    """A Tibber home with methods to get/fetch home information without the decorator functions to subscribe to live data."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    def fetch_consumption(self, 
                          resolution: str, 
                          first: int = None, 
                          last: int = None, 
                          before: str = None, 
                          after: str = None, 
                          filter_empty_nodes: bool = False) -> HomeConsumptionConnection:
        consumption_query = QueryBuilder.consumption_query(resolution, first, last, before, after, filter_empty_nodes)
        full_query = QueryBuilder.create_query("viewer", f"home(id: \"{self.id}\")", consumption_query)
        unsanitized_data = self.tibber_client.execute_query(self.tibber_client.token, full_query)

        # The format should be correct, since we requested it this way and the request
        # was successful, so we don't need to worry about key errors. 
        data = unsanitized_data["viewer"]["home"]["consumption"]
        return HomeConsumptionConnection(resolution, data, self.tibber_client)

    def fetch_production(self,
                         resolution: str = None, 
                         first: int = None, 
                         last: int = None, 
                         before: str = None, 
                         after: str = None, 
                         filter_empty_nodes: bool = False) -> HomeProductionConnection:
        production_query = QueryBuilder.production_query(resolution, first, last, before, after, filter_empty_nodes)
        full_query = QueryBuilder.create_query("viewer", f"home(id: \"{self.id}\")", production_query)
        unsanitized_data = self.tibber_client.execute_query(self.tibber_client.token, full_query)
        
        data = unsanitized_data["viewer"]["home"]["production"]
        return HomeProductionConnection(resolution, data, self.tibber_client)

    @property
    def id(self) -> str:
        return self.cache.get("id")

    @property
    def time_zone(self) -> str:
        return self.cache.get("timeZone")

    @property
    def app_nickname(self) -> str:
        return self.cache.get("appNickname")

    @property
    def app_avatar(self) -> str:
        return self.cache.get("appAvatar")

    @property
    def size(self) -> int:
        return self.cache.get("size")

    @property
    def type(self) -> str:
        return self.cache.get("type")

    @property
    def number_of_residents(self) -> int:
        return self.cache.get("numberOfResidents")

    @property
    def primary_heating_source(self) -> str:
        return self.cache.get("primaryHeatingSource")

    @property
    def has_ventilation_system(self) -> bool:
        return self.cache.get("hasVentilationSystem")

    @property
    def main_fuse_size(self) -> int:
        return self.cache.get("mainFuseSize")

    @property
    def owner(self) -> LegalEntity:
        return LegalEntity(self.cache.get("owner"), self.tibber_client)

    @property
    def metering_point_data(self) -> MeteringPointData:
        return MeteringPointData(self.cache.get("meteringPointData"), self.tibber_client)

    @property
    def current_subscription(self) -> Subscription:
        return Subscription(self.cache.get("currentSubscription"), self.tibber_client)
    
    @property
    def subscriptions(self) -> list:
        return [Subscription(sub, self.tibber_client) for sub in self.cache.get("subscriptions", [])]
    
    @property
    def features(self):
        return HomeFeatures(self.cache.get("features"), self.tibber_client)
    
    # Support 1 to 1 Tibber API representation.
    @property
    def address(self) -> Address:
        return Address(self.cache.get("address"), self.tibber_client)
    
    @property
    def address1(self) -> str:
        return self.address.address1

    @property
    def address2(self) -> str:
        return self.address.address2

    @property
    def address3(self) -> str:
        return self.address.address3

    @property
    def city(self) -> str:
        return self.address.city

    @property
    def postal_code(self) -> str:
        return self.address.postal_code

    @property
    def country(self) -> str:
        return self.address.country

    @property
    def latitude(self) -> str:
        return self.address.latitude

    @property
    def longitude(self) -> str:
        return self.address.longitude

class TibberHome(NonDecoratedTibberHome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()
        self._callbacks = {}

    def event(self, event_to_listen_for) -> Callable:
        def decorator(callback):
            # Initialize webhook if there is not already.
            
            if event_to_listen_for == "consumption":
                # Create the consumption key if it does not exist already
                if not ("consumption" in self._callbacks):
                    self._callbacks["consumption"] = []
                # Append the callback function to the dict of callbacks
                self._callbacks["consumption"].append(callback)

            else: 
                raise ValueError(f"Could not recognize the event you want to listen for: {event_to_listen_for}")
            return callback
        return decorator
        
        
    def start_livefeed(self):
        """Creates a websocket and starts pushing data out to registered callbacks."""
        self.tibber_client.eventloop.run_until_complete(self.run_websocket_loop())
        
    async def run_websocket_loop(self):
        async with websockets.connect(SUBSCRIPTION_ENDPOINT, subprotocols=["graphql-ws"]) as websocket:
            pass