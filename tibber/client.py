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
        self.token: str = token

        super()

        if immediate_update:
            # TODO: Check if the token is valid
            self.init_update()

    def init_update(self):
        """Updates all information and caches it."""
        self.execute_query(QueryBuilder.update_all_info)

    @property
    def cache(self) -> dict:
        return self.cache

    @property
    def token(self) -> str:
        return self.token

    @token.setter
    def token(self, token: str):
        if self.token:
            raise AttributeError("Can't set token once it has already been set.")
        if not isinstance(token, str):
            raise TypeError("The token must be a string.")
        self.token = token
        