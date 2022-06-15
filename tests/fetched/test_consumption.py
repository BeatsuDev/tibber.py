"""Tests for fetching consumption data from the API."""
from datetime import datetime
from datetime import timedelta

import pytest

import tibber


@pytest.fixture
def home():
    client = tibber.Client(tibber.DEMO_TOKEN)
    try:
        return client.homes[0]
    except IndexError:
        raise ValueError("The instanciated demo client does not have any homes. Cannot perform home tests.")

def test_consumption_page_info(home):
    home_consumption_connection = home.fetch_consumption("HOURLY", first=4, after="MjAyMC0wNC0yN1QxOTowMDowMC4wMDArMDI6MDA=")
    page_info = home_consumption_connection.page_info

    assert page_info.end_cursor == home_consumption_connection.edges[-1].cursor
    assert page_info.has_next_page
    assert page_info.has_previous_page
    assert page_info.start_cursor == home_consumption_connection.edges[0].cursor

    assert page_info.count == 4
    assert page_info.currency == "NOK"
    assert page_info.total_cost == 0.6131657916666666
    assert page_info.total_consumption == 4.401
    assert page_info.filtered == 0

def test_consumption_nodes(home):
    home_consumption_connection = home.fetch_consumption("HOURLY", first=5)
    history = home_consumption_connection.nodes

    assert history[0].from_time == "2020-04-27T00:00:00.000+02:00"
    assert history[0].to_time == "2020-04-27T01:00:00.000+02:00"

    assert [node.unit_price for node in history] == [0.0913625, 0.0903625, 0.0903625, 0.0905, 0.09165]
    assert [node.unit_price_vat for node in history] == [0.0182725, 0.0180725, 0.0180725, 0.0181, 0.01833]
    assert [node.consumption_unit == "kWh" for node in history]

