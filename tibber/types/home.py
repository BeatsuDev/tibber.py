"""Classes representing the Home type from the GraphQL Tibber API."""
from tibber.types.legal_entity import LegalEntity
from tibber.types.address import Address
from tibber.types.metering_point_data import MeteringPointData
from tibber.types.subscription import Subscription


class TibberHome:
    """A Tibber home with methods to get/fetch home information without the decorator functions to subscribe to live data."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def id(self) -> str:
        return self.cache.get("id")

    @property
    def time_zone(self) -> str:
        return self.cache.get("timeZone")

    @property
    def app_nickname(self) -> str:
        return self.cache.get("appNickname")

    @property
    def app_avatar(self) -> str:
        return self.cache.get("appAvatar")

    @property
    def size(self) -> int:
        return self.cache.get("size")

    @property
    def type(self) -> str:
        return self.cache.get("type")

    @property
    def number_of_residents(self) -> int:
        return self.cache.get("numberOfResidents")

    @property
    def primary_heating_source(self) -> str:
        return self.cache.get("primaryHeatingSource")

    @property
    def has_ventilation_system(self) -> bool:
        return self.cache.get("hasVentilationSystem")

    @property
    def main_fuse_size(self) -> int:
        return self.cache.get("mainFuseSize")

    @property
    def owner(self) -> LegalEntity:
        return LegalEntity(self.cache.get("owner"), self.tibber_client)

    @property
    def metering_point_data(self) -> MeteringPointData:
        return MeteringPointData(self.cache.get("meteringPointData"), self.tibber_client)

    @property
    def current_subscription(self) -> Subscription:
        return Subscription(self.cache.get("currentSubscription"), self.tibber_client)
    
    @property
    def subscriptions(self) -> list[Subscription]:
        return [Subscription(sub) for sub in self.cache.get("subscriptions", [])]
    
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
        return self.address.address2

    @property
    def address3(self) -> str:
        return self.address.address3

    @property
    def city(self) -> str:
        return self.address.city

    @property
    def postal_code(self) -> str:
        return self.address.postal_code

    @property
    def country(self) -> str:
        return self.address.country

    @property
    def latitude(self) -> str:
        return self.address.latitude

    @property
    def longitude(self) -> str:
        return self.address.longitude


class DecoratedTibberHome(TibberHome):
    """A Tibber home with methods to get/fetch home information and decorators to subscribe to real time data."""
    pass