from typing import Optional

import aiohttp


class QueryExecutor:
    """A class for executing sessions."""
    def __init__(self, websession: Optional[aiohttp.ClientSession] = None):
        """Instantiates the query executor. This creates a websession among other things."""
        self.websession = websession if websession else aiohttp.ClientSession()
        from tibber import API_ENDPOINT

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

        return asyncio.run(send_request(post_args))

    async def send_request(self, post_args: dict, retries: int = 3):
        """Sends a request to the Tibber API.

        :param post_args: The arguments to send in the Tibber API web request. The post args should
            contain a "headers" key with the access token authorization and a "data" key with.
        :param retries: The amount of retries to attempt before raising an asyncio Timeout error.
        """
        # TODO: Handle errors
        resp = await self.websession.post(API_ENDPOINT, **post_args)

        if errors := result.get("errors"):
            # TODO: Handle errors
            pass

        result = await resp.json()
        return result

    @property
    def websession(self):
        return websession

    @websession.setter
    def websession(self):
        # TODO: Close the websession before setting it to a new one.
        pass

    @property
    def user_agent(self):
        return user_agent