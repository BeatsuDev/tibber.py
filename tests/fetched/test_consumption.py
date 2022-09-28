"""Tests for fetching consumption data from the API."""
from datetime import datetime
from datetime import timedelta

import pytest

import tibber


@pytest.fixture
def home():
    account = tibber.Account(tibber.DEMO_TOKEN)
    try:
        return account.homes[0]
    except IndexError:
        raise ValueError("The instanciated demo account does not have any homes. Cannot perform home tests.")

def test_consumption_page_info(home):
    home_consumption_connection = home.fetch_consumption("HOURLY", first=5, after="MjAxOC0xMS0wM1QyMDowMDowMC4wMDArMDE6MDA=")
    page_info = home_consumption_connection.page_info

    assert page_info.end_cursor == home_consumption_connection.edges[-1].cursor
    assert page_info.has_next_page
    assert page_info.has_previous_page
    assert page_info.start_cursor == home_consumption_connection.edges[0].cursor

    assert page_info.count == 5
    assert page_info.currency == "SEK"
    assert page_info.total_cost == 6.151398125
    assert page_info.total_consumption == 9.45
    assert page_info.filtered == 0

def test_consumption_nodes(home):
    home_consumption_connection = home.fetch_consumption("HOURLY", first=5)
    history = home_consumption_connection.nodes

    assert history[0].from_time == "2018-11-02T00:00:00.000+01:00"
    assert history[0].to_time == "2018-11-02T01:00:00.000+01:00"

    assert [node.unit_price for node in history] == [0.6300375, 0.614075, 0.61175, 0.6085375, 0.6163875]
    assert [node.unit_price_vat for node in history] == [0.1260075, 0.122815, 0.12235, 0.1217075, 0.1232775]
    assert all(node.consumption_unit == "kWh" for node in history)

