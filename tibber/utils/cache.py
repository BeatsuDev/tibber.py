"""Contains a cache class for storing dicts and retrieving values from nested dicts."""
from typing import Any

class Cache(dict):
    """A dict with an overriden get() method."""
    def __init__(self, data: dict = {}):
        super().__init__(data)
        self.data = data
        
    def get(self, *keys, default: Any = None, _dict_to_get_from: dict = None):
        """Gets the values from cache after entering the given keys to traverse the dict with. Returns None if the "path" does not exist.
        
        :param keys: The keys to access when traversing the dict.
        :param dict_to_get_from: An alternative dict to get from. This paramter is used recursively in this method and should not be used outside.
        
        Example usage:
            a = {"foo": {"bar": True}}
            a.get("foo", "bar") # True
        """
        data = dict_to_get_from or self.data
        if len(keys) == 0: return None
        if len(keys) == 1: return data.get(keys[0])

        if not isinstance(first_value := data.get(keys[0]), dict):
            return None

        return self.get(*keys[1:], _dict_to_get_from=first_value)