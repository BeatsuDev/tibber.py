"""A class representing the PushNotificationResponse type from the GraphQL Tibber API."""


class PushNotificationResponse:
    def __init__(self, data: dict, tibber_client: "Client"):
        self.data = data or {}

    @property
    def successful(self):
        return self.data.get("successful")
    
    @property
    def pushed_to_number_of_devices(self):
        return self.data.get("pushedToNumberOfDevices")