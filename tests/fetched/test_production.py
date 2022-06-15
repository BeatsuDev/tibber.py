"""Tests for fetching production data from the API."""
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

def test_production_page_info(home):
    home_production_connection = home.fetch_production("HOURLY", first=10, after="MjAyMi0wNi0xNFQxMzowMDowMC4wMDArMDI6MDA=")
    page_info = home_production_connection.page_info

    assert page_info.end_cursor == home_production_connection.edges[-1].cursor
    assert page_info.has_next_page
    assert page_info.has_previous_page
    assert page_info.start_cursor == home_production_connection.edges[0].cursor

    assert page_info.count == 10
    assert page_info.currency == "NOK"
    assert page_info.total_profit == 1.33715513
    assert page_info.total_production == 10.035
    assert page_info.filtered == 0

def test_production_nodes(home):
    home_production_connection = home.fetch_production("HOURLY", last=5)
    history = home_production_connection.nodes

    for i, hour in enumerate(history):
        from_time = datetime.strptime(hour.from_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        to_time = datetime.strptime(hour.to_time, "%Y-%m-%dT%H:%M:%S.%f%z")

        ft = datetime.now().astimezone().replace(minute=0, second=0, microsecond=0)
        ft -= timedelta(hours=1+(4 - i))
        tt = datetime.now().astimezone().replace(minute=0, second=0, microsecond=0)
        tt -= timedelta(hours=(4 - i))

        assert from_time == ft
        assert to_time == tt

    assert [node.production_unit == "kWh" for node in history]