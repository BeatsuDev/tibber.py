from tibber.networking import QueryExecutor
from tibber.networking import QueryBuilder

class Client(QueryExecutor):
    """The main Tibber class to communicate with the Tibber API."""
    def __init__(self, token: str, immediate_update: bool=True):
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
        data = self.execute_query(self.token, QueryBuilder.update_all_info)
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

    # Client data gathered from cache
    @property
    def name(self):
        # TODO: Error handling if the key does not exist
        return self.cache["viewer"].get("name")

    @property
    def login(self):
        # TODO: Error handling if the key does not exist
        return self.cache["viewer"].get("login")

    @property
    def user_id(self):
        # TODO: Error handling if the key does not exist
        return self.cache["viewer"].get("userId")

    @property
    def account_type(self):
        # TODO: Error handling if the key does not exist
        return self.cache["viewer"].get("accountType")
    
    @property
    def homes(self):
        from tibber import TibberHome
        # TODO: Error handling if the key does not exist
        return [ TibberHome(data, self) for data in self.cache["viewer"]["homes"] ]