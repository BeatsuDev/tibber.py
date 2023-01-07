import logging
import dataclasses
from typing import Any

from gqlrequests_api_tibber import RootQuery, RootMutation, Viewer
from gqlrequests.query import Query
from gqlrequests.query_method import QueryMethod

from .networking import QueryExecutor
from .types.push_notification_response import PushNotificationResponse

_logger = logging.getLogger(__name__)

class Account(QueryExecutor):
    """The main Tibber class to communicate with the Tibber API."""
    def __init__(self, token: str, user_agent: str = None, immediate_update: bool = True):
        """Initialize the tibber client.

        :param token: The token to log in with
        :param immediate_update: Specifies whether to immediately update all tibber information 
            on initialization.
        :throws UnauthenticatedException: If the provided token was not accepted by the Tibber API.
            Note that this will only be checked if the immediate_update parameter is set to True.
        """
        self.data: Viewer = None
        self._token: str = token
        self.user_agent = user_agent

        super().__init__()

        if immediate_update:
            self.fetch_all()
    
    def __getattr__(self, attribute: str) -> Any:
        return dataclasses.asdict(super().__getattribute__("data"))[attribute]

    async def update_async(self, retries = 1):
        """Fetches all available data from the API and caches it. This method is used in async
        contexts to avoid errors about an event loop already running."""
        data = await self.execute_async(self.token, str(Query(RootQuery)), retries)
        self.update_cache(data)

    def fetch_all(self, retries = 1):
        """Fetches all available data from the API and caches it."""
        data = self.execute_query(self.token, str(Query(RootQuery)))
        self.data = Viewer(**data.get("viewer"))

    def update(self):
        """Alias for fetch_all()"""
        self.fetch_all()

    def send_push_notification(self, title: str, message: str, screen_to_open: str = None):
        """Sends a push notification to all registered devices connected to the account owning the API key."""
        response_data = self.execute_query(self.token, Query(RootMutation, fields=[
            QueryMethod("sendPushNotification", args={"title": title, "message": message, "screenToOpen": screen_to_open})
        ]))
        return PushNotificationResponse(**response_data)

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str):
        if not isinstance(token, str):
            _logger.error("Attempted to set the token to a non-string datatype: " + type(token))
            raise TypeError("The token must be a string.")
        self._token = token
        _logger.debug("The tibber token was set to a new value.")
    