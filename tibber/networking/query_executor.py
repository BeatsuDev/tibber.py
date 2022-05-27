import asyncio
import logging
import json
from typing import Optional

import aiohttp

from tibber import API_ENDPOINT
from tibber.exceptions import APIException


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

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        post_args = self.create_request(access_token, query)
        return self.eventloop.run_until_complete(self.send_request(post_args))
    
    def execute_mutation(self, access_token: str, data: str, retries: int = 3):
        """Executes a GraphQL mutation to the Tibber API.

        :param access_token: The Tibber API token to use for the request.
        :param data: The mutation to send to the Tibber API.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        post_args = self.create_request(access_token, data, "mutation")
        return self.eventloop.run_until_complete(self.send_request(post_args))
        
    
    def create_request(self, access_token: str, data: str, request_type: str = "query"):
        """Creates a GraphQL request, but does not execute it. Returns a dict that can
        be passed to the send_request method.
        
        :param access_token: The access token to use for the request.
        :param data: The data to be sent in the request.
        :param request_type: The root type of the request (e.g. "mutation" or "query").
        """
        # TODO: Implement query variables
        payload = {request_type: data, "variables": {}} 

        request = {
            "headers": {
                "Authorization": "Bearer " + access_token
            },
            "data": payload,
        }
        return request

    async def send_request(self, post_args: dict, retries: int = 3):
        """Sends a request to the Tibber API.

        :param post_args: The arguments to send in the Tibber API web request. The post args should
            contain a "headers" key with the access token authorization and a "data" key with.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        # Log the request we are making (and redact the access token in case users share the logs)
        if self.logger.level == logging.DEBUG:
            from copy import deepcopy
            debug_post_args = deepcopy(post_args)
            debug_post_args["headers"]["Authorization"] = "Bearer <## TOKEN REDACTED ##>"
            self.logger.debug("Executing a query with these post args:\n" + debug_post_args)

        resp = await self.websession.post(API_ENDPOINT, **post_args)
        result = await resp.json()
        
        self.logger.debug("Response received. The json data is:\n" + json.dumps(result))

        errors = result.get("errors")
        if errors:
            # TODO: Handle errors better
            print(errors)
            raise APIException("Something went wrong with the request.ERRORS:\n" + "\n".join(e.get("message") for e in errors))

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