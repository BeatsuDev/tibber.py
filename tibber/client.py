from tibber.networking import QueryExecutor
from tibber.networking import QueryBuilder
from tibber.types.viewer import Viewer

class Client(QueryExecutor):
    """The main Tibber class to communicate with the Tibber API."""
    def __init__(self, token: str, immediate_update: bool = True):
        """Initialize the tibber client.

        :param token: The token to log in with
        :param immediate_update: Specifies whether to immediately update all tibber information 
            on initialization.
        :throws InvalidToken: If the provided token was not accepted by the Tibber API. Note
            that this will only be checked if the immediate_update parameter is set to True.
        """
        self.cache: dict = {}
        self._token: str = token

        super().__init__()

        if immediate_update:
            # TODO: Check if the token is valid
            self.initial_update()

    def initial_update(self):
        """Updates all information and caches it."""
        data = self.execute_query(self.token, QueryBuilder.query_all_data)
        # TODO: Move cache update to when the query is executed and successful
        self.cache = QueryBuilder.combine_dicts(self.cache, data)

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str):
        if self.token:
            raise AttributeError("Can't set token once it has already been set.")
        if not isinstance(token, str):
            raise TypeError("The token must be a string.")
        self.token = token
        
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
        return self.viewer.user_id

    @property
    def account_type(self):
        return self.viewer.account_type
    
    @property
    def homes(self):
        return self.viewer.homes