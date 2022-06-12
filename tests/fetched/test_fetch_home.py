"""Tests for fetching tibber.TibberHome properties from the API"""
import pytest

import tibber


@pytest.fixture
def home():
    client = tibber.Client(tibber.DEMO_TOKEN)
    try:
        return client.homes[0]
    except IndexError:
        raise ValueError("The instanciated demo client does not have any homes. Cannot perform home tests.")


def test_fetch_first_5_hourly_consumption_nodes(home):
    edge = home.fetch_consumption("HOURLY", first=5)
    history = edge.nodes

    assert history[0].from_time == "2020-04-27T00:00:00.000+02:00"
    assert history[0].to_time == "2020-04-27T01:00:00.000+02:00"

    assert [n.unit_price for n in history] == [0.0913625, 0.0903625, 0.0903625, 0.0905, 0.09165]