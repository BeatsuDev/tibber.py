"""A class representing the Viewer type from the GraphQL Tibber API."""
from tibber.types.home import TibberHome


class Viewer:
    """A class to get information about the viewer."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client
        
    @property
    def name(self):
        return self.cache.get("name")

    @property
    def login(self):
        return self.cache.get("login")

    @property
    def user_id(self):
        return self.cache.get("userId")

    @property
    def account_type(self):
        return self.cache.get("accountType")
    
    @property
    def homes(self):
        return [ TibberHome(home, self.tibber_client) for home in self.cache.get("homes", []) ]