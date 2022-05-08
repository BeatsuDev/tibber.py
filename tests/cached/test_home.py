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

def test_reading_id(home):
    assert home.id == "cc83e83e-8cbf-4595-9bf7-c3cf192f7d9c"
    
def test_reading_time_zome(home):
    assert home.time_zone == "Europe/Oslo"
    
def test_reading_app_nickname(home):
    assert home.app_nickname == "Ulltang casa"
    
def test_reading_size(home):
    assert home.size == 200
    
def test_reading_type(home):
    assert home.type == "HOUSE"
    
def test_reading_number_of_residents(home):
    assert home.number_of_residents == 4
    
def test_reading_primary_heating_source(home):
    assert home.primary_heating_source == "AIR2AIR_HEATPUMP"
    
def test_reading_has_ventilation_system(home):
    assert home.has_ventilation_system == True
    
def test_reading_main_fuse_size(home):
    assert home.main_fuse_size == 63

def test_reading_owner(home):
    assert isinstance(home.owner, LegalEntity)

def test_reading_metering_point_data(home):
    assert isinstance(home.metering_point_data, MeteringPointData)

def test_reading_current_subscription(home):
    assert isinstance(home.current_subscription, Subscription)

def test_reading_subscriptions(home):
    assert len(home.subscriptions) == 2
    assert isinstance(home.subscriptions[0], Subscription)

def test_reading_features(home):
    assert isinstance(home.features, HomeFeatures)
    
def test_reading_address(home):
    assert isinstance(home.address, Address)
