import asyncio
import logging
import json
from typing import Optional

import aiohttp

from tibber import API_ENDPOINT


class QueryExecutor:
    """A class for executing sessions."""
    def __init__(self, websession: Optional[aiohttp.ClientSession] = None):
        """Instantiates the query executor. This creates a websession among other things."""
        self.logger = logging.getLogger(__name__)
        
        try:
            self.eventloop = asyncio.get_running_loop()
        except RuntimeError:
            self.logger.debug("No running event loop was found. Creating a new one with asyncio.get_event_loop()")
            self.eventloop = asyncio.get_event_loop()

        self.eventloop.run_until_complete(self.__async_init__(websession))
        
    async def __async_init__(self, websession: Optional[aiohttp.ClientSession] = None):
        if websession:
            self._websession = websession
        else:
            self.logger.debug("A websession was not provided. Creating a new aiohttp.ClientSession.")
            self._websession = aiohttp.ClientSession()

    def execute_query(self, access_token: str, query: str, retries: int = 3):
        """Executes a GraphQL query to the Tibber API.

        :param query: The query to send to the Tibber API.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        # Create post args
        # TODO: Implement query variables
        payload = {"query": query, "variables": {}} 

        post_args = {
            "headers": {
                "Authorization": "Bearer " + access_token
            },
            "data": payload,
        }

        if self.logger.level == logging.DEBUG:
            # Redact the access token in the debug message in case users share log files with others.
            from copy import deepcopy
            debug_post_args = deepcopy(post_args)
            debug_post_args["headers"]["Authorization"] = "Bearer <## TOKEN REDACTED ##>"
            self.logger.debug("Executing a query with these post args:\n" + debug_post_args)

        return self.eventloop.run_until_complete(self.send_request(post_args))

    async def send_request(self, post_args: dict, retries: int = 3):
        """Sends a request to the Tibber API.

        :param post_args: The arguments to send in the Tibber API web request. The post args should
            contain a "headers" key with the access token authorization and a "data" key with.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        resp = await self.websession.post(API_ENDPOINT, **post_args)
        result = await resp.json()
        
        self.logger.debug("Response received. The json data is:\n" + json.dumps(result))

        errors = result.get("errors")
        if errors:
            # TODO: Handle errors better
            raise APIException("Something went wrong with the request.\n\nErrors:\n" + errors)

        return result.get("data")

    @property
    def websession(self):
        return self._websession

    @websession.setter
    def websession(self):
        # TODO: Close the websession before setting it to a new one.
        pass
    
    def __del__(self):
        """Close the websession when the class is deloaded"""
        if self.eventloop.is_closed(): return
        if self.websession.closed: return
        self.eventloop.run_until_complete(self.websession.close())