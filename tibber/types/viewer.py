"""A class representing the Viewer type from the GraphQL Tibber API."""
from tibber.types.home import TibberHome


class Viewer:
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data or {}
        self.tibber_client: "Client" = tibber_client
        
    @property
    def name(self):
        return self.cache.get("name")

    @property
    def login(self):
        return self.cache.get("login")

    @property
    def user_id(self):
        """Unique user identifier"""
        return self.cache.get("userId")

    @property
    def account_type(self):
        """The type of account for the logged-in user."""
        return self.cache.get("accountType")
    
    @property
    def homes(self):
        """All homes visible to the logged-in user"""
        return [ TibberHome(home, self.tibber_client) for home in self.cache.get("homes", []) ]
    
    # TODO: Implement home(id: ID!): Home! method. (get_home and fetch_home)