from typing import Optional

import aiohttp


class QueryExecutor:
    """A class for executing sessions"""
    def __init__(self, websession: Optional[aiohttp.ClientSession] = None):
        """"""
        self.websession = websession