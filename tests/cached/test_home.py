"""Tests for reading tibber.TibberHome properties from cached values after the Tibber client is initialized."""
import pytest

import tibber
from tibber.types import LegalEntity
from tibber.types import MeteringPointData
from tibber.types import Subscription
from tibber.types import HomeFeatures
from tibber.types import Address


@pytest.fixture
def home():
    client = tibber.Client(tibber.DEMO_TOKEN)
    try:
        return client.homes[0]
    except IndexError:
        raise ValueError("The instanciated demo client does not have any homes. Cannot perform home tests.")

def test_getting_id(home):
    assert home.id == "cc83e83e-8cbf-4595-9bf7-c3cf192f7d9c"
    
def test_getting_time_zome(home):
    assert home.time_zone == "Europe/Oslo"
    
def test_getting_app_nickname(home):
    assert home.app_nickname == "Ulltang casa"
    
def test_getting_size(home):
    assert home.size == 200
    
def test_getting_type(home):
    assert home.type == "HOUSE"
    
def test_getting_number_of_residents(home):
    assert home.number_of_residents == 4
    
def test_getting_primary_heating_source(home):
    assert home.primary_heating_source == "AIR2AIR_HEATPUMP"
    
def test_getting_has_ventilation_system(home):
    assert home.has_ventilation_system == True
    
def test_getting_main_fuse_size(home):
    assert home.main_fuse_size == 63

def test_getting_owner(home):
    assert isinstance(home.owner, LegalEntity)

def test_getting_metering_point_data(home):
    assert isinstance(home.metering_point_data, MeteringPointData)

    # TODO: Move to an own test file
    data = home.metering_point_data
    assert data.consumption_ean == "707057500084125027"
    assert data.grid_company == "Sunnfjord Energi AS Nett"
    assert data.grid_area_code == "50YK05ZHDDCGA4AK"
    assert data.price_area_code == "NO3"
    assert data.production_ean == "707057500084125027P"
    assert data.energy_tax_type == "none"

def test_getting_current_subscription(home):
    assert isinstance(home.current_subscription, Subscription)

def test_getting_subscriptions(home):
    assert len(home.subscriptions) == 2
    assert isinstance(home.subscriptions[0], Subscription)

def test_getting_features(home):
    assert isinstance(home.features, HomeFeatures)
    
def test_getting_address(home):
    assert isinstance(home.address, Address)
    
def test_getting_address1(home):
    assert home.address1 == "Winterfell Castle 1"
