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
    home_consumption_connection = home.fetch_consumption("HOURLY", first=5, after="MjAyMi0xMS0yOFQxODowMDowMC4wMDArMDE6MDA=")
    page_info = home_consumption_connection.page_info

    assert page_info.end_cursor == home_consumption_connection.edges[-1].cursor
    assert page_info.has_next_page
    assert page_info.has_previous_page
    assert page_info.start_cursor == home_consumption_connection.edges[0].cursor

    assert page_info.count == 5
    assert page_info.currency == "SEK"
    assert page_info.total_cost == 39.5775870375
    assert page_info.total_consumption == 15.132
    assert page_info.filtered == 0

def test_consumption_nodes(home):
    home_consumption_connection = home.fetch_consumption("HOURLY", first=3, after="MjAyMi0xMS0yOFQxODowMDowMC4wMDArMDE6MDA=")
    history = home_consumption_connection.nodes

    assert history[0].from_time == "2022-11-28T19:00:00.000+01:00"
    assert history[0].to_time == "2022-11-28T20:00:00.000+01:00"

    assert [node.cost for node in history] == [7.95558735, 8.85535695, 7.205103525]
    assert [node.unit_price for node in history] == [3.09195, 2.854725, 2.689475]
    assert [node.unit_price_vat for node in history] == [0.61839, 0.570945, 0.537895]
    assert [node.consumption for node in history] == [2.573, 3.102, 2.679]
    assert all(node.consumption_unit == "kWh" for node in history)

