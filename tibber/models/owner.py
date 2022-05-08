from tibber.utils import Cache

class HomeOwner:
    def __init__(self, data: dict, tibber_client: "TibberClient"):
        self.cache = Cache(data)