"""Tests to verify home features data"""
import pytest

import tibber


@pytest.fixture
def home():
    client = tibber.Client(tibber.DEMO_TOKEN)
    try:
        return client.homes[0]
    except IndexError:
        raise ValueError("The instanciated demo client does not have any homes. Cannot perform home tests.")


def test_real_time_consumption(home):
    assert home.features.real_time_consumption_enabled