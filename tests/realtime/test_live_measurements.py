"""Tests for reading live data from a tibber.TibberHome"""
import pytest
from datetime import datetime
from datetime import timedelta

import tibber
from tibber import __version__
from tibber.types.live_measurement import LiveMeasurement


def test_adding_listener_with_unknown_event_raises_exception(home):
    with pytest.raises(ValueError):
        @home.event("invalid-event-name")
        async def callback(data):
            print(data)

def test_starting_live_feed_with_no_listeners_shows_warning(caplog):
    account = tibber.Account(tibber.DEMO_TOKEN)
    home = account.homes[0]

    # Return immediately after the first callback
    home.start_live_feed(f"tibber.py-tests/{__version__}", exit_condition = lambda data: True)
    assert "The event that was broadcasted has no listeners / callbacks! Nothing was run." in caplog.text

def test_retrieving_live_measurements():
    account = tibber.Account(tibber.DEMO_TOKEN)
    home = account.homes[0]

    global callback_was_run
    callback_was_run = False
    @home.event("live_measurement")
    async def callback(data):
        global callback_was_run
        callback_was_run = True
        assert isinstance(data, LiveMeasurement)
        timestamp = datetime.strptime(data.timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        timestamp = timestamp.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)
        assert timestamp > now - timedelta(seconds=30)
        assert data.power > 0
        assert data.last_meter_consumption > 0
        assert data.accumulated_consumption > 0
        assert isinstance(data.accumulated_production, (int, float))
        assert data.accumulated_consumption_last_hour > 0
        assert isinstance(data.accumulated_production_last_hour, (int, float))
        assert data.accumulated_cost > 0
        assert isinstance(data.accumulated_reward, (int, float))
        assert data.currency == "SEK"
        assert data.min_power >= 0
        assert data.max_power > 0
        assert data.average_power > 0
        assert isinstance(data.power_production, (int, float))
        assert isinstance(data.power_reactive, (int, float))
        assert data.power_production_reactive > 0
        assert isinstance(data.min_power_production, (int, float))
        assert isinstance(data.max_power_production, (int, float))
        assert data.last_meter_production > 0
        assert data.power_factor > 0
        assert data.voltage_phase_1 > 0
        assert data.voltage_phase_2 > 0
        assert data.voltage_phase_3 > 0
        assert data.currentL1 > 0
        assert data.currentL2 > 0
        assert data.currentL3 > 0

    # Return immediately after the first callback
    home.start_live_feed(f"tibber.py-tests/{__version__}", exit_condition = lambda data: True)
    assert callback_was_run
