"""Tests for reading data from cached values after the Tibber client is initialized."""
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import pytest

import tibber


@pytest.fixture
def client():
    return tibber.Client(tibber.DEMO_TOKEN)


def test_reading_viewer_info(client):
    assert client.name == "Arya Stark"
    assert client.login == "edgeir@tibber.com"
    assert client.user_id == "df4b53bf-0709-4679-8744-08876cbb03c1"
    assert client.account_type == ["tibber", "customer"]
    # client.homes is tested in test_reading_home_info


def test_reading_home_info(client):
    assert len(client.homes) == 1
    assert isinstance(client.homes[0], tibber.TibberHome)

    home = client.homes[0]

    assert home.id == "cc83e83e-8cbf-4595-9bf7-c3cf192f7d9c"
    assert home.time_zone == "Europe/Oslo"
    assert home.app_nickname == "Ulltang casa"
    assert home.app_avatar == "FLOORHOUSE2"
    assert home.size == 200
    assert home.type == "HOUSE"
    assert home.number_of_residents == 4
    assert home.primary_heating_source == "AIR2AIR_HEATPUMP"
    assert home.has_ventilation_system == True
    assert home.main_fuse_size == 63
