"""Tests for reading live data from a tibber.TibberHome"""
import pytest
from datetime import datetime
from datetime import timedelta

import tibber


@pytest.fixture
def home():
    client = tibber.Client(tibber.DEMO_TOKEN)
    try:
        return client.homes[0]
    except IndexError:
        raise ValueError("The instanciated demo client does not have any homes. Cannot perform home tests.")


def test_realtime_live_measurements(home):  
    import time
    start_time = time.perf_counter()

    @home.event("live_measurement")
    def callback(data):
        timestamp = datetime.strptime(data.timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        # This *might* cause errors on really slow networks. 
        assert (datetime.now().astimezone() - timestamp) < timedelta(seconds=5)
        raise RuntimeError("Exit the loop!")

    with pytest.raises(RuntimeError):
        home.start_livefeed()

def test_adding_listener_with_unknown_event_raises_exception(home):
    with pytest.raises(ValueError):
        @home.event("invalid-event-name")
        def callback(data):
            print(data)