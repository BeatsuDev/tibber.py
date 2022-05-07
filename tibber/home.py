"""Classes for retrieving data of a Tibber Home"""


class TibberHome:
    """A Tibber home with methods to get/fetch home information without the decorator functions to subscribe to live data."""
    def __init__(self, data: dict, tibber_client: "TibberClient"):
        self.cache = data
        self.tibber_client = tibber_client


    @property
    def id(self):
        return self.cache.get("id")

    @property
    def time_zone(self):
        return self.cache.get("timeZone")

    @property
    def app_nickname(self):
        return self.cache.get("appNickname")

    @property
    def app_avatar(self):
        return self.cache.get("appAvatar")

    @property
    def size(self):
        return self.cache.get("size")

    @property
    def type(self):
        return self.cache.get("type")

    @property
    def number_of_residents(self):
        return self.cache.get("numberOfResidents")

    @property
    def primary_heating_source(self):
        return self.cache.get("primaryHeatingSource")

    @property
    def has_ventilation_system(self):
        return self.cache.get("hasVentilationSystem")

    @property
    def main_fuse_size(self):
        return self.cache.get("mainFuseSize")
    
    # TODO: Add other values as well


class DecoratedTibberHome(TibberHome):
    """A Tibber home with methods to get/fetch home information and decorators to subscribe to real time data."""
    pass