"""Classes representing the Home type from the GraphQL Tibber API."""
import json
import asyncio
import logging
from typing import Callable
from typing import TYPE_CHECKING

import websockets

from tibber import SUBSCRIPTION_ENDPOINT
from tibber.types.legal_entity import LegalEntity
from tibber.types.address import Address
from tibber.types.metering_point_data import MeteringPointData
from tibber.types.subscription import Subscription
from tibber.types.home_features import HomeFeatures
from tibber.types.live_measurement import LiveMeasurement
from tibber.types.home_consumption_connection import HomeConsumptionConnection
from tibber.types.home_production_connection import HomeProductionConnection
from tibber.networking import QueryBuilder

# Import type checking modules
if TYPE_CHECKING:
    from tibber.client import Client 


class NonDecoratedTibberHome:
    """A Tibber home with methods to get/fetch home information without the decorator functions to subscribe to live data."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data or {}
        self.tibber_client: "Client" = tibber_client
        
        # Logging
        self.logger = logging.getLogger(__name__)

    def fetch_consumption(self, 
                          resolution: str, 
                          first: int = None, 
                          last: int = None, 
                          before: str = None, 
                          after: str = None, 
                          filter_empty_nodes: bool = False) -> HomeConsumptionConnection:
        """Consumption connection"""
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
        """The time zone the home resides in"""
        return self.cache.get("timeZone")

    @property
    def app_nickname(self) -> str:
        """The nickname given to the home by the user"""
        return self.cache.get("appNickname")

    @property
    def app_avatar(self) -> str:
        """The chosen avatar for the home"""
        return self.cache.get("appAvatar")

    @property
    def size(self) -> int:
        """The size of the home in square meters"""
        return self.cache.get("size")

    @property
    def type(self) -> str:
        """The type of home."""
        return self.cache.get("type")

    @property
    def number_of_residents(self) -> int:
        """The number of people living in the home"""
        return self.cache.get("numberOfResidents")

    @property
    def primary_heating_source(self) -> str:
        """The primary form of heating in the household"""
        return self.cache.get("primaryHeatingSource")

    @property
    def has_ventilation_system(self) -> bool:
        """Whether the home has a ventilation system"""
        return self.cache.get("hasVentilationSystem")

    @property
    def main_fuse_size(self) -> int:
        """The main fuse size"""
        return self.cache.get("mainFuseSize")

    @property
    def owner(self) -> LegalEntity:
        """The registered owner of the house"""
        return LegalEntity(self.cache.get("owner"), self.tibber_client)

    @property
    def metering_point_data(self) -> MeteringPointData:
        return MeteringPointData(self.cache.get("meteringPointData"), self.tibber_client)

    @property
    def current_subscription(self) -> Subscription:
        """The current/latest subscription related to the home"""
        return Subscription(self.cache.get("currentSubscription"), self.tibber_client)
    
    @property
    def subscriptions(self) -> list:
        """All historic subscriptions related to the home"""
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
        """Returns a decorator that registers the function being
        decorated as a callback function for the given event
        
        :param event_to_listen_for: The event the decorator should register the function
            as a callback for.
        """
        def decorator(callback):
            """Returns the function as it is, but registers it as a callback for an event.
            
            :param callback: The function being decorated.
            :throws ValueError: if the given event is not a valid event.
            """
            if event_to_listen_for == "live_measurement":
                # Create the live_measurement key if it does not exist already
                if not ("live_measurement" in self._callbacks):
                    self._callbacks["live_measurement"] = []
                # Append the callback function to the dict of callbacks
                self._callbacks["live_measurement"].append(callback)

            else: 
                raise ValueError(f"Could not recognize the event you want to listen for: {event_to_listen_for}")
            return callback
        return decorator
        
        
    def start_livefeed(self):
        """Creates a websocket and starts pushing data out to registered callbacks."""
        self.tibber_client.eventloop.run_until_complete(self.run_websocket_loop())
        
    async def run_websocket_loop(self):
        """Starts a websocket."""
        # Tell the websocket that we are wanting to connect
        connection_init_message = json.dumps(
            {"type": "connection_init", "payload": {}}
        )
            
        # Request the data we want
        root_subscription_query = QueryBuilder.live_measurement(self.id)
        request_message = json.dumps(
            {"type": "start", "id": "1", "payload": {"query": root_subscription_query}}
        )
        
        # Connect the websocket, then fire off the created requests
        async with websockets.connect(
            SUBSCRIPTION_ENDPOINT,
            subprotocols=["graphql-ws"],
            extra_headers={"Authorization": self.tibber_client.token}
        ) as websocket:
            self.logger.debug("Sending initial payloads to start connection with live data websocket.")
            self.logger.debug("Connection init message:\n" + connection_init_message)
            self.logger.debug("Request message:\n" + request_message)
            
            await websocket.send(connection_init_message)
            await websocket.send(request_message)

            # Now we should be receiving data!
            async for data in websocket:
                dict_data = json.loads(data)
                self.process_websocket_response(dict_data)

    def process_websocket_response(self, data):
        """Processes a response with data from the live data websocket."""
        if data["type"] == "connection_ack":
            self.logger.debug("Retrieved connection_ack. The websocket connection was accepted.")
            return
        
        elif data["type"] == "ka":
            self.logger.debug("Received ka (Keep Alive) from websocket.")
            return
        
        elif data["type"] == "error":
            # TODO: Better error handling
            raise Exception("Something went wrong: " + data["payload"]["message"])
            
        # Broadcast the event
        # TODO: Differentiate between consumption data, production data and other data.
        self.broadcast_event("live_measurement", LiveMeasurement(data["payload"]["data"]["liveMeasurement"], self.tibber_client))
                    
    def broadcast_event(self, event, data):
        if not event in self._callbacks:
            self.logger.warning("The event that was broadcasted has no listeners / callbacks! Nothing was run.")
            return
        
        for callback in self._callbacks[event]:
            callback(data)