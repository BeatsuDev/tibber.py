"""Tests for reading tibber.Client properties from cached values after the Tibber client is initialized."""
import pytest

import tibber
from tibber.types import NonDecoratedTibberHome
from tibber.types import Viewer
from tibber.exceptions import InvalidTokenException


@pytest.fixture
def client():
    return tibber.Client(tibber.DEMO_TOKEN)

def test_getting_viewer(client):
    assert isinstance(client.viewer, Viewer)

def test_getting_name(client):
    assert client.name == "Arya Stark"
    
def test_getting_login(client):
    assert client.login == "edgeir@tibber.com"
    
def test_getting_user_id(client):
    assert client.user_id == "df4b53bf-0709-4679-8744-08876cbb03c1"

def test_getting_account_type(client):
    assert client.account_type == ["tibber", "customer"]
    
def test_getting_homes(client):
    assert len(client.homes) == 1
    
def test_homes_are_correct_type(client):
    assert all(isinstance(home, NonDecoratedTibberHome) for home in client.homes)

def test_incorrect_token():
    with pytest.raises(InvalidTokenException):
        client = tibber.Client("invalidtoken")

def test_getting_non_fetched_property_returns_none_or_empty():
    """Trying to get a value which has not yet been fetched should return None"""
    client = tibber.Client(tibber.DEMO_TOKEN, False)
    assert client.name == None
    assert client.viewer.homes == []