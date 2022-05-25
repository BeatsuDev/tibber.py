"""A class representing the LiveMeasurement type from the GraphQL Tibber API."""


class LiveMeasurement:
    """A class containing the live household electricity information."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client

    @property
    def timestamp(self) -> str:
        return self.cache.get("timestamp")

    @property
    def power(self) -> float:
        return self.cache.get("power")

    @property
    def last_meter_consumption(self) -> float:
        return self.cache.get("lastMeterConsumption")

    @property
    def accumulated_consumption(self) -> float:
        return self.cache.get("accumulatedConsumption")

    @property
    def accumulated_production(self) -> float:
        return self.cache.get("accumulatedProduction")

    @property
    def accumulated_consumption_last_hour(self) -> float:
        return self.cache.get("accumulatedConsumptionLastHour")

    @property
    def accumulated_production_last_hour(self) -> float:
        return self.cache.get("accumulatedProductionLastHour")

    @property
    def accumulated_cost(self) -> float:
        return self.cache.get("accumulatedCost")

    @property
    def accumulated_reward(self) -> float:
        return self.cache.get("accumulatedReward")

    @property
    def currency(self) -> str:
        return self.cache.get("currency")

    @property
    def min_power(self) -> float:
        return self.cache.get("minPower")

    @property
    def average_power(self) -> float:
        return self.cache.get("averagePower")

    @property
    def max_power(self) -> float:
        return self.cache.get("maxPower")

    @property
    def power_production(self) -> float:
        return self.cache.get("powerProduction")

    @property
    def power_reactive(self) -> float:
        return self.cache.get("powerReactive")

    @property
    def power_production_reactive(self) -> float:
        return self.cache.get("powerProductionReactive")

    @property
    def min_power_production(self) -> float:
        return self.cache.get("minPowerProduction")

    @property
    def max_power_production(self) -> float:
        return self.cache.get("maxPowerProduction")

    @property
    def last_meter_production(self) -> float:
        return self.cache.get("lastMeterProduction")

    @property
    def power_factor(self) -> float:
        return self.cache.get("powerFactor")

    @property
    def voltage_phase_1(self) -> float:
        return self.cache.get("voltagePhase1")

    @property
    def voltage_phase_2(self) -> float:
        return self.cache.get("voltagePhase2")

    @property
    def voltage_phase_3(self) -> float:
        return self.cache.get("voltagePhase3")

    @property
    def currentL1(self) -> float:
        return self.cache.get("currentL1")

    @property
    def currentL2(self) -> float:
        return self.cache.get("currentL2")

    @property
    def currentL3(self) -> float:
        return self.cache.get("currentL3")

    @property
    def signal_strength(self) -> int:
        return self.cache.get("signalStrength")