"""Classes representing the Home type from the GraphQL Tibber API."""
import json
import asyncio
import logging
from typing import Union
from typing import Callable
from typing import TYPE_CHECKING

import websockets
import backoff
import gql
from gql.transport.websockets import WebsocketsTransport
from gql.transport.exceptions import TransportQueryError
from graphql import parse

from tibber import __version__
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
    from tibber.account import Account 


_logger = logging.getLogger(__name__)

class NonDecoratedTibberHome:
    """A Tibber home with methods to get/fetch home information without the decorator functions to subscribe to live data."""
    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

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
        return self.address.address2  # pragma: no cover

    @property
    def address3(self) -> str:
        return self.address.address3  # pragma: no cover

    @property
    def city(self) -> str:
        return self.address.city  # pragma: no cover

    @property
    def postal_code(self) -> str:
        return self.address.postal_code  # pragma: no cover

    @property
    def country(self) -> str:
        return self.address.country  # pragma: no cover

    @property
    def latitude(self) -> str:
        return self.address.latitude  # pragma: no cover

    @property
    def longitude(self) -> str:
        return self.address.longitude  # pragma: no cover

class TibberHome(NonDecoratedTibberHome):
    """A Tibber home with methods to get/fetch home information and subscribe to live data.
    This class expands on the NonDecoratedTibberHome class by adding methods to subscribe to live data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._websocket_client = None
        self.websocket_running = False
        self._callbacks = {}

    def event(self, event_to_listen_for) -> Callable:
        """Returns a decorator that registers the function being
        decorated as a callback function for the given event

        :param event_to_listen_for: The event the decorator should register the function as a callback for.
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

    def start_live_feed(self, user_agent = None, exit_condition: Callable[[LiveMeasurement], bool] = None, retries: int = 3, retry_interval: Union[float, int] = 10, **kwargs) -> None:
        """Creates a websocket and starts pushing data out to registered callbacks.

        :param exit_condition: A function that takes a LiveMeasurement as input and returns a boolean.
            If the function returns True, the websocket will be closed.
        :param retries: The number of times to retry connecting to the websocket if it fails.
        :param retry_interval: The interval in seconds to wait before retrying to connect to the websocket.
        :param kwargs: Additional arguments to pass to the websocket (gql.transport.WebsocketsTransport).
        """
        if not self.features.real_time_consumption_enabled:
            raise ValueError("The home does not have real time consumption enabled.")

        if not self.tibber_client.user_agent and not user_agent:
            raise ValueError("You must specify a user agent when starting the live feed. E.g. \"Homey/10.0.0\"")

        self.tibber_client.user_agent = user_agent or self.tibber_client.user_agent
        try:
            asyncio.run(self.start_websocket_loop(exit_condition, retries = retries, **kwargs))
        except KeyboardInterrupt:  # pragma: no cover
            print("Closing websocket...")
        finally:
            self.close_websocket_connection()

    async def start_websocket_loop(self, exit_condition: Callable[[LiveMeasurement], bool] = None, retries: int = 3, retry_interval: Union[float, int] = 10, **kwargs) -> None:
        """Starts a websocket to subscribe for live measurements.
        
        :param exit_condition: A function that takes a LiveMeasurement as input and returns a boolean.
            If the function returns True, the websocket will be closed.
        :param retries: The number of times to retry connecting to the websocket if it fails.
        :param retry_interval: The interval in seconds to wait before retrying to connect to the websocket.
        :param kwargs: Additional arguments to pass to the websocket (gql.transport.WebsocketsTransport).
        """
        if retry_interval < 1:
            raise ValueError("The retry interval must be at least 1 second.")

        # Create the websocket
        transport = WebsocketsTransport(
            **kwargs,
            url = self.tibber_client.viewer.websocket_subscription_url,
            subprotocols = ["graphql-transport-ws"],
            init_payload = {"token": self.tibber_client.token},
            headers = {"User-Agent": f"{self.tibber_client.user_agent} tibber.py/{__version__}"},
        )

        self._websocket_client = gql.Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        retry = backoff.on_exception(
            backoff.expo,
            Exception,
            max_value = 100,
            max_tries = retries,
            jitter = backoff.full_jitter,
            giveup = lambda e: isinstance(e, TransportQueryError),
        )

        self.websocket_running = True
        print("Connecting to websocket")
        session = await self._websocket_client.connect_async(
            reconnecting = True,
            retry_connect = retry,
            retry_execute = retry,
        )
        await retry(self.run_websocket_loop)(session, exit_condition)

    async def run_websocket_loop(self, session, exit_condition):
        # Subscribe to the websocket
        query = QueryBuilder.live_measurement(self.id)
        _logger.debug(f"Connecting to live measurement data endpoint with query: {' '.join(query.split())}")
        document_node_query = parse(query)

        _logger.info("Subscribing to websocket.")
        async for data in session.subscribe(document_node_query):
            _logger.debug("real time data received.")

            # Returns True if exit condition is met
            if self.process_websocket_response(data, exit_condition=exit_condition):
                _logger.info("Exit condition met.")
                break

        self.close_websocket_connection()


    def process_websocket_response(self, data: dict, exit_condition: Callable[[LiveMeasurement], bool] = None) -> bool:
        """Processes a response with data from the live data websocket. This function will call all registered callbacks
        before checking if the exit condition is met.

        :param data: The data to process.
        :return: Returns True if exit condition was met. False otherwise.
        """
        # Broadcast the event
        # TODO: Differentiate between consumption data, production data and other data.
        cleaned_data = LiveMeasurement(data["liveMeasurement"], self.tibber_client)
        self.broadcast_event("live_measurement", cleaned_data)

        # Check if the exit condition is met
        if exit_condition and exit_condition(cleaned_data):
            return True
        return False

    def broadcast_event(self, event, data) -> None:
        if not event in self._callbacks:
            _logger.warning("The event that was broadcasted has no listeners / callbacks! Nothing was run.")
            return

        for callback in self._callbacks[event]:
            callback(data)

    def close_websocket_connection(self):
        _logger.info("Closing websocket connection")
        self.websocket_running = False
        if self._websocket_client:
            asyncio.run(self._websocket_client.close_async())
            self._websocket_client = None  # Dereference for gc
        else:
            _logger.debug("self._websocket_client was not defined when attempting to close the websocket.")
