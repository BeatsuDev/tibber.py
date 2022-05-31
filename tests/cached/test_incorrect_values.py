"""Tests for asserting "wrong" behaviour is handled correctly. For example,
wrong token, getting data which hasn't been fetched before etc."""
import pytest

import tibber
from tibber.exceptions import InvalidTokenException


@pytest.fixture
def client():
    return tibber.Client(tibber.DEMO_TOKEN)

def test_incorrect_token():
    with pytest.raises(InvalidTokenException):
        client = tibber.Client("invalidtoken")

def test_getting_non_fetched_property_returns_none_or_empty():
    """Trying to get a value which has not yet been fetched should return None"""
    client = tibber.Client(tibber.DEMO_TOKEN, False)
    assert client.name == None
    assert client.viewer.homes == []
