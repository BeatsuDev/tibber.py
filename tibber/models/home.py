"""Classes for retrieving data of a Tibber Home"""
from tibber.models import HomeOwner
from tibber.utils import Cache

class TibberHome:
    """A Tibber home with methods to get/fetch home information without the decorator functions to subscribe to live data."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: "Cache" = Cache(data)
        self.tibber_client: "Client" = tibber_client

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

    @property
    def owner(self):
        return self.cache.get("owner")

    @property
    def metering_point_data(self):
        return self.cache.get("meteringPointData")

    @property
    def subscription(self):
        return self.cache.get("currentSubscription")
    
    # Support 1 to 1 Tibber API representation.
    @property
    def address(self):
        return self.cache.get("address")
    
    @property
    def address1(self):
        return self.cache.get("address", "address1")

    @property
    def address2(self):
        return self.cache.get("address", "address2")

    @property
    def address3(self):
        return self.cache.get("address", "address3")

    @property
    def city(self):
        return self.cache.get("address", "city")

    @property
    def postal_code(self):
        return self.cache.get("address", "postalCode")

    @property
    def country(self):
        return self.cache.get("address", "country")

    @property
    def latitude(self):
        return self.cache.get("address", "latitude")

    @property
    def longitude(self):
        return self.cache.get("address", "longitude")


class DecoratedTibberHome(TibberHome):
    """A Tibber home with methods to get/fetch home information and decorators to subscribe to real time data."""
    pass