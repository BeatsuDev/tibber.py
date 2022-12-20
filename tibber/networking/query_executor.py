import asyncio
import logging
import json
from typing import Optional

import aiohttp

from tibber import API_ENDPOINT
from tibber.exceptions import APIException
from tibber.exceptions import InvalidTokenException


_logger = logging.getLogger(__name__)

class QueryExecutor:
    """A class for executing sessions."""
    def __init__(self, websession: Optional[aiohttp.ClientSession] = None):
        """Instantiates the query executor. This creates a websession among other things."""
        self._websession = websession or aiohttp.ClientSession()

    def execute_query(self, access_token: str, query: str, retries: int = 2):
        """Executes a GraphQL query to the Tibber API.

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        post_args = self.create_request(access_token, query)
        return asyncio.run(self.send_request(post_args, retries))

    def create_request(self, access_token: str, data: str):
        """Creates a GraphQL request, but does not execute it. Returns a dict that can
        be passed to the send_request method.
        
        :param access_token: The access token to use for the request.
        :param data: The data to be sent in the request.
        :param request_type: The root type of the request (e.g. "mutation" or "query").
        """
        # TODO: Implement query variables
        payload = {"query": data, "variables": {}} 

        request = {
            "headers": {
                "Authorization": "Bearer " + access_token
            },
            "data": payload,
        }
        return request

    async def send_request(self, post_args: dict, retries: int = 2):
        """Sends a request to the Tibber API.

        :param post_args: The arguments to send in the Tibber API web request. The post args should
            contain a "headers" key with the access token authorization and a "data" key with.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        # TODO: Only run deepcopy if the logger level is DEBUG.
        # Log the request we are making (and redact the access token in case users share the logs)
        from copy import deepcopy
        debug_post_args = deepcopy(post_args)
        debug_post_args["headers"]["Authorization"] = "Bearer <## TOKEN REDACTED ##>"
        debug_query = debug_post_args["data"]["query"]
        debug_post_args["data"]["query"] = "<QUERY>"
        _logger.debug("Executing a query with these post args:\n" + json.dumps(debug_post_args) + "\nWhere <QUERY> is:\n" + debug_query)

        json_response = {}
        times_attempted = 0
        while not json_response.get("data") and times_attempted <= retries:
            if times_attempted > 0:
                _logger.info(f"Failed to retrieve data from api request. Retrying ({times_attempted} of {retries} times).")

            response = await self.websession.post(API_ENDPOINT, **post_args)
            json_response = await response.json()
            _logger.debug("Response from API request received. The json data is:\n" + json.dumps(json_response, indent=4))

            errors = json_response.get("errors")
            if errors:
                # TODO: Handle errors better
                # For now, errors are simply logged since the method can still return data although there's an error. (see issue #6)
                _logger.error(f"Something went wrong with the request. The following errors occured:\n{json.dumps(errors, indent=4)}")
                
                # InvalidToken:
                if "UNAUTHENTICATED" in map(lambda e: e["extensions"]["code"], errors):
                    raise InvalidTokenException("Could not authenticate with the given token!")

            times_attempted += 1

        if not json_response.get("data"):
            raise APIException(f"Something went wrong with the request. The following errors occured:\n{json.dumps(errors, indent=4)}")

        return json_response.get("data")

    @property
    def websession(self):
        return self._websession
    
    def __del__(self):
        """Close the websession when the class is deloaded"""
        if self.websession.closed: return
        asyncio.run(self.websession.close())
