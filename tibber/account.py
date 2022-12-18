import logging
import json

from .networking import QueryExecutor
from .networking import QueryBuilder
from .types.viewer import Viewer
from .types.push_notification_response import PushNotificationResponse

_logger = logging.getLogger(__name__)
class Account(QueryExecutor):
    """The main Tibber class to communicate with the Tibber API."""
    def __init__(self, token: str, user_agent: str = None, immediate_update: bool = True):
        """Initialize the tibber client.

        :param token: The token to log in with
        :param immediate_update: Specifies whether to immediately update all tibber information 
            on initialization.
        :throws InvalidToken: If the provided token was not accepted by the Tibber API. Note
            that this will only be checked if the immediate_update parameter is set to True.
        """
        self.cache: dict = {}
        self._token: str = token
        self.user_agent = user_agent

        _logger.debug("Do you see this?")
        print(__name__)

        super().__init__()

        if immediate_update:
            self.fetch_all()

    def fetch_all(self):
        """Fetches all available data from the API and caches it."""
        data = self.execute_query(self.token, QueryBuilder.query_all_data)
        self.update_cache(data)

    def update_cache(self, data):
        """Updates the cache with values from data.
        
        :param data: The data to add / update values in the cache with.
        """
        _logger.debug("Overwriting the cache data.")
        _logger.debug("Old data: " + json.dumps(self.cache))
        _logger.debug("New data: " + json.dumps(data))
        self.cache = QueryBuilder.combine_dicts(self.cache, data)

    def send_push_notification(self, title: str, message: str, screen_to_open: str = None):
        """Sends a push notification to all registered devices connected to the account owning the API key."""
        data = QueryBuilder.send_push_notification(title, message, screen_to_open)
        response_data = self.execute_query(self.token, data).get("sendPushNotification")
        return PushNotificationResponse(response_data, self)

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str):
        if not isinstance(token, str):
            _logger.error("Attempted to set the token to a non-string datatype: " + type(token))
            raise TypeError("The token must be a string.")
        self._token = token
        _logger.debug("The tibber token was set to: " + token)
        
    @property
    def viewer(self):
        return Viewer(self.cache.get("viewer"), self)

    @property
    def name(self):
        return self.viewer.name

    @property
    def login(self):
        return self.viewer.login

    @property
    def user_id(self):
        """Unique user identifier"""
        return self.viewer.user_id

    @property
    def account_type(self):
        """The type of account for the logged-in user."""
        return self.viewer.account_type
    
    @property
    def homes(self):
        """All homes visible to the logged-in user"""
        return self.viewer.homes