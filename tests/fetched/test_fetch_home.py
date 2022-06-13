"""Tests for fetching tibber.TibberHome properties from the API"""
from datetime import datetime
from datetime import timedelta
from matplotlib import ft2font

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

def test_fetch_first_5_hourly_production_nodes(home):
    edge = home.fetch_production("HOURLY", last=5)
    history = edge.nodes

    for i, hour in enumerate(history):
        from_time = datetime.strptime(hour.from_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        to_time = datetime.strptime(hour.to_time, "%Y-%m-%dT%H:%M:%S.%f%z")

        ft = datetime.now().astimezone().replace(minute=0, second=0, microsecond=0)
        ft -= timedelta(hours=1+(4 - i))
        tt = datetime.now().astimezone().replace(minute=0, second=0, microsecond=0)
        tt -= timedelta(hours=(4 - i))

        assert from_time == ft
        assert to_time == tt