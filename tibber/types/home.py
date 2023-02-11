from __future__ import annotations

"""Classes representing the Home type from the GraphQL Tibber API."""
import random
import asyncio
import inspect
import logging
from typing import TYPE_CHECKING, Callable, Union

import gql
import websockets
from gql.transport.exceptions import TransportQueryError
from gql.transport.websockets import WebsocketsTransport
from graphql import parse

from tibber import __version__
from tibber.networking import QueryBuilder
from tibber.types.address import Address
from tibber.types.home_consumption_connection import HomeConsumptionConnection
from tibber.types.home_features import HomeFeatures
from tibber.types.home_production_connection import HomeProductionConnection
from tibber.types.legal_entity import LegalEntity
from tibber.types.live_measurement import LiveMeasurement
from tibber.types.metering_point_data import MeteringPointData
from tibber.types.subscription import Subscription

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


_logger = logging.getLogger(__name__)


class NonDecoratedTibberHome:
    """A Tibber home with methods to get/fetch home information without the decorator functions to subscribe to live data."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    def fetch_consumption(
        self,
        resolution: str,
        first: int = None,
        last: int = None,
        before: str = None,
        after: str = None,
        filter_empty_nodes: bool = False,
    ) -> HomeConsumptionConnection:
        """Consumption connection"""
        consumption_query = QueryBuilder.consumption_query(
            resolution, first, last, before, after, filter_empty_nodes
        )
        full_query = QueryBuilder.create_query(
            "viewer", f'home(id: "{self.id}")', consumption_query
        )
        unsanitized_data = self.tibber_client.execute_query(
            self.tibber_client.token, full_query
        )

        # The format should be correct, since we requested it this way and the request
        # was successful, so we don't need to worry about key errors.
        data = unsanitized_data["viewer"]["home"]["consumption"]
        return HomeConsumptionConnection(resolution, data, self.tibber_client)

    def fetch_production(
        self,
        resolution: str = None,
        first: int = None,
        last: int = None,
        before: str = None,
        after: str = None,
        filter_empty_nodes: bool = False,
    ) -> HomeProductionConnection:
        production_query = QueryBuilder.production_query(
            resolution, first, last, before, after, filter_empty_nodes
        )
        full_query = QueryBuilder.create_query(
            "viewer", f'home(id: "{self.id}")', production_query
        )
        unsanitized_data = self.tibber_client.execute_query(
            self.tibber_client.token, full_query
        )

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
        return MeteringPointData(
            self.cache.get("meteringPointData"), self.tibber_client
        )

    @property
    def current_subscription(self) -> Subscription:
        """The current/latest subscription related to the home"""
        return Subscription(self.cache.get("currentSubscription"), self.tibber_client)

    @property
    def subscriptions(self) -> list:
        """All historic subscriptions related to the home"""
        return [
            Subscription(sub, self.tibber_client)
            for sub in self.cache.get("subscriptions", [])
        ]

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
        self._callbacks = {"live_measurement": []}

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
            # Check if callback is a coroutine
            if not inspect.iscoroutinefunction(callback):
                raise ValueError(
                    "Callback functions must be coroutines! Use the `async def` syntax, instead of just `def`."
                )

            # If the key is not found - the event is not a valid event!
            # Valid events will be added directly to the line where _callbacks is initialized.
            try:
                self._callbacks[event_to_listen_for].append(callback)
            except KeyError:
                raise ValueError(
                    f"Could not recognize the event you want to listen for: {event_to_listen_for}"
                )

            return callback

        return decorator

    def start_live_feed(
        self,
        user_agent=None,
        exit_condition: Callable[[LiveMeasurement], bool] = None,
        retries: int = 5,
        on_connection_error: Callable[[Exception], None] = None,
        on_query_error: Callable[[Exception], None] = None,
        **kwargs,
    ) -> None:
        """Creates a websocket and starts pushing data out to registered callbacks.

        :param user_agent: The user agent to use when connecting to the websocket.
        :param exit_condition: A function that takes a LiveMeasurement as input and returns a boolean.
            If the function returns True, the websocket will be closed.
        :param retries: The number of times to retry connecting to the websocket if it fails.
        :param on_connection_error: A function that is run when an error occurs while connecting to the websocket.
            This will be called every time a connection attempt fails.
        :param on_query_error: A function that is run when query to the websocket returns an error.
            This will be called every time a query fails.
        :param kwargs: Additional arguments to pass to the websocket (gql.transport.WebsocketsTransport).
        """
        if not self.features.real_time_consumption_enabled:
            raise ValueError("The home does not have real time consumption enabled.")

        if not self.tibber_client.user_agent and not user_agent:
            raise ValueError(
                'You must specify a user agent when starting the live feed. E.g. "Homey/10.0.0"'
            )

        self.tibber_client.user_agent = user_agent or self.tibber_client.user_agent

        # The folllowing code is just to run the websocket loop in the correct loop.
        websocket_loop_coroutine = self.start_websocket_loop(
            exit_condition, retries=retries, on_exception=on_exception, **kwargs
        )
        _run_async_in_correct_event_loop(websocket_loop_coroutine)

    def _run_async_in_correct_event_loop(self, coroutine):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return loop.run_until_complete(coroutine)
        else:
            return asyncio.run(coroutine)

    async def start_websocket_loop(
        self,
        exit_condition: Callable[[LiveMeasurement], bool] = None,
        retries: int = 5,
        on_query_error: Callable[[Exception], None] = None,
        **kwargs,
    ) -> None:
        """Starts a websocket to subscribe for live measurements.

        :param exit_condition: A function that takes a LiveMeasurement as input and returns a boolean.
            If the function returns True, the websocket will be closed.
        :param retries: The number of times to retry connecting to the websocket if it fails.
        :param on_query_error: A function that is run when query to the websocket returns an error.
            This will be called every time a query fails.
        :param kwargs: Additional arguments to pass to the websocket (gql.transport.WebsocketsTransport).
        """
        # Create the websocket
        transport = WebsocketsTransport(
            **kwargs,
            url=self.tibber_client.viewer.websocket_subscription_url,
            subprotocols=[WebsocketsTransport.GRAPHQLWS_SUBPROTOCOL],
            init_payload={"token": self.tibber_client.token},
            headers={
                "User-Agent": f"{self.tibber_client.user_agent} tibber.py/{__version__}"
            },
        )

        self._websocket_client = gql.Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )

        # Connect to the websocket
        _logger.debug("connecting to websocket")
        session = await self._websocket_client.connect_async(
            reconnecting=True,
            retry_connect=retry_connect,
        )
        _logger.info("Connected to websocket.")

        # Subscribe to the websocket
        await self._run_websocket_loop(session, exit_condition)
        await session.close_async()

    async def _run_websocket_loop(self, session, exit_condition) -> None:
        # Check if real time consumption is enabled
        _logger.info(
            "Updating home information to check if real time consumption is enabled."
        )
        await self.tibber_client.update_async()

        if not self.features.real_time_consumption_enabled:
            raise ValueError("The home does not have real time consumption enabled.")

        # Subscribe to the websocket
        query = QueryBuilder.live_measurement(self.id)
        _logger.debug(
            f"Connecting to live measurement data endpoint with query: {' '.join(query.split())}"
        )
        document_node_query = parse(query)

        _logger.info("Subscribing to websocket.")
        async for data in session.subscribe(document_node_query):
            _logger.debug("real time data received.")

            # Returns True if exit condition is met
            exit_condition_met = await self._process_websocket_response(
                data, exit_condition=exit_condition
            )
            if exit_condition_met:
                _logger.info("Exit condition met. The live loop is now exiting.")
                break

    async def _process_websocket_response(
        self, data: dict, exit_condition: Callable[[LiveMeasurement], bool] = None
    ) -> bool:
        """Processes a response with data from the live data websocket. This function will call all registered callbacks
        before checking if the exit condition is met.

        :param data: The data to process.
        :return: Returns True if exit condition was met. False otherwise.
        """
        # Broadcast the event
        # TODO: Differentiate between consumption data, production data and other data.
        cleaned_data = LiveMeasurement(data["liveMeasurement"], self.tibber_client)
        await self._broadcast_event("live_measurement", cleaned_data)

        # Check if the exit condition is met
        if exit_condition and exit_condition(cleaned_data):
            return True
        return False

    async def _broadcast_event(self, event, data) -> None:
        if event not in self._callbacks:
            _logger.warning(
                f'The event "{event}" was attempted emitted, but does not exist. Nothing was run.'
            )

        if len(self._callbacks[event]) == 0:
            _logger.warning(
                "The event that was broadcasted has no listeners / callbacks! Nothing was run."
            )
            return

        await asyncio.gather(*[c(data) for c in self._callbacks[event]])

    @property
    def websocket_running(self) -> bool:
        """Returns True if the websocket is running. False otherwise."""
        return (
            self._websocket_client is not None
            and isinstance(self._websocket_client.transport, WebsocketsTransport)
            and self._websocket_client.transport.websocket is not None
            and self._websocket_client.transport.websocket.open
        )
