"""Contains a cache class for storing dicts and retrieving values from nested dicts."""

class Cache(dict):
    def __init__(self, data: dict = {}):
        super().__init__(data)
        self.data = data
        
    def get(self, *keys, dict_to_get_from: dict = None):
        """Gets the values from cache after entering the given keys to traverse the dict with. Returns None if the "path" does not exist."""
        data = dict_to_get_from or self.data
        if len(keys) == 0: return None
        if len(keys) == 1: return data.get(keys[0])

        if not isinstance(first_value := data.get(keys[0]), dict):
            return None

        return self.get(*keys[1:], dict_to_get_from=first_value)