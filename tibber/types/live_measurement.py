from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class LiveMeasurement:
    """A dataclass representing the LiveMeasurement type from the GraphQL Tibber API."""
    timestamp: str = field(default=None)
    power: float = field(default=None)
    last_meter_consumption: float = field(default=None)
    accumulated_consumption: float = field(default=None)
    accumulated_production: float = field(default=None)
    accumulated_consumption_last_hour: float = field(default=None)
    accumulated_production_last_hour: float = field(default=None)
    accumulated_cost: float = field(default=None)
    accumulated_reward: float = field(default=None)
    currency: str = field(default=None)
    min_power: float = field(default=None)
    average_power: float = field(default=None)
    max_power: float = field(default=None)
    power_production: float = field(default=None)
    power_reactive: float = field(default=None)
    power_production_reactive: float = field(default=None)
    power_factor: float = field(default=None)
    voltage_phase_1: float = field(default=None)
    voltage_phase_2: float = field(default=None)
    voltage_phase_3: float = field(default=None)
    current_l1: float = field(default=None)
    current_l2: float = field(default=None)
    current_l3: float = field(default=None)
