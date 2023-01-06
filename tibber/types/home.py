from __future__ import annotations
import json
import asyncio
import logging
from dataclasses import dataclass, field

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


_logger = logging.getLogger(__name__)

@dataclass
class Home:
    """A dataclass representing the Home type from the GraphQL Tibber API with methods to get/fetch home
    information and the decorator functions to subscribe to live data."""
    id: str | None = field(default=None)
    time_zone: str | None = field(default=None)
    app_nickname: str | None = field(default=None)
    app_avatar: str | None = field(default=None)
    size: int | None = field(default=None)
    type: str | None = field(default=None)
    number_of_residents: int | None = field(default=None)
    primary_heating_source: str | None = field(default=None)
    has_ventilation_system: bool | None = field(default=None)
    main_fuse_size: int | None = field(default=None)
    address: Address = field(default=None)
    owner: LegalEntity = field(default=None)
    metering_point_data: MeteringPointData = field(default=None)
    current_subscription: Subscription = field(default=None)
    subscriptions: list[Subscription] = field(default_factory=list)
    features: HomeFeatures = field(default=None)

    consumption: HomeConsumptionConnection = field(default=None)
    production: HomeProductionConnection = field(default=None)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._websocket_client = None
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
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        try:
            if loop and loop.is_running():
                loop.run_until_complete(self.start_websocket_loop(exit_condition, retries = retries, **kwargs))
            else:
                asyncio.run(self.start_websocket_loop(exit_condition, retries = retries, **kwargs))
        except KeyboardInterrupt:
            _logger.info("Keyboard interrupt detected. Websocket should be closed now.")

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
            subprotocols = [WebsocketsTransport.GRAPHQLWS_SUBPROTOCOL],
            init_payload = {"token": self.tibber_client.token},
            headers = {"User-Agent": f"{self.tibber_client.user_agent} tibber.py/{__version__}"},
            ping_interval=10,
            pong_timeout=10,
        )

        self._websocket_client = gql.Client(    
            transport = transport,
            fetch_schema_from_transport = True,
        )

        retry_connect = backoff.on_exception(
            backoff.expo,
            [gql.transport.exceptions.TransportClosed, websockets.exceptions.ConnectionClosedError],
            max_value = 100,
            max_tries = retries,
            on_backoff = lambda details: _logger.warning("Retrying to connect with backoff. Running {target} in {wait:.1f} seconds after {tries} tries.".format(**details)),
            jitter = backoff.full_jitter,
            giveup = lambda e: isinstance(e, TransportQueryError) or isinstance(e, ValueError),
        )

        retry_subscribe = backoff.on_exception(
            backoff.expo,
            Exception,
            max_value = 100,
            max_tries = retries,
            on_backoff = lambda details: _logger.warning("Retrying to subscribe with backoff. Running {target} in {wait:.1f} seconds after {tries} tries.".format(**details)),
            jitter = backoff.full_jitter,
            giveup = lambda e: isinstance(e, TransportQueryError) or isinstance(e, ValueError),
        )

        _logger.debug("connecting to websocket")
        session = await self._websocket_client.connect_async(
            reconnecting = True,
            retry_connect = retry_connect,
        )
        _logger.info("Connected to websocket.")
        await retry_subscribe(self.run_websocket_loop)(session, exit_condition)

    async def run_websocket_loop(self, session, exit_condition) -> None:
        # Check if real time consumption is enabled
        _logger.info("Updating home information to check if real time consumption is enabled.")
        await self.tibber_client.update_async()

        if not self.features.real_time_consumption_enabled:
            raise ValueError("The home does not have real time consumption enabled.")

        # Subscribe to the websocket
        query = QueryBuilder.live_measurement(self.id)
        _logger.debug(f"Connecting to live measurement data endpoint with query: {' '.join(query.split())}")
        document_node_query = parse(query)

        _logger.info("Subscribing to websocket.")
        async for data in session.subscribe(document_node_query):
            _logger.debug("real time data received.")

            # Returns True if exit condition is met
            if self.process_websocket_response(data, exit_condition=exit_condition):
                _logger.info("Exit condition met. The live loop is now exiting.")
                break

        await self.close_websocket_connection()

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

    async def close_websocket_connection(self) -> None:
        _logger.debug("attempting to close websocket connection")
        if self.websocket_running:
            try:
                await self._websocket_client.close_async()
                self._websocket_client = None  # Dereference for gc
                _logger.info("Websocket connection closed.")
            except KeyboardInterrupt as e:
                _logger.warning("Keyboard interrupt detected while closing wbsocket connection. This may cause the websocket to be left open.")
                raise e
        else:
            _logger.info(
                "The websocket was not running when attempting to close the websocket." +
                " The invocation of close_websocket_connection() therefore did nothing...")
    
    @property
    def websocket_running(self) -> bool:
        """Returns True if the websocket is running. False otherwise."""
        return (
            self._websocket_client is not None and 
            isinstance(self._websocket_client.transport, WebsocketsTransport) and
            self._websocket_client.transport.websocket is not None and
            self._websocket_client.transport.websocket.open
        )


class NonDecoratedTibberHome:

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
