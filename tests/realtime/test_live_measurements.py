"""Tests for reading live data from a tibber.TibberHome"""
import pytest
from datetime import datetime
from datetime import timedelta

import tibber


@pytest.fixture
def home():
    account = tibber.Account(tibber.DEMO_TOKEN)
    try:
        return account.homes[0]
    except IndexError:
        raise ValueError("The instanciated demo account does not have any homes. Cannot perform home tests.")

def test_adding_listener_with_unknown_event_raises_exception(home):
    with pytest.raises(ValueError):
        @home.event("invalid-event-name")
        def callback(data):
            print(data)