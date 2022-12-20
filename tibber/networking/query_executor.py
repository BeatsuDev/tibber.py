import asyncio
import logging
import json
from typing import Optional

import backoff
import gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from tibber import API_ENDPOINT
from tibber.exceptions import APIException
from tibber.exceptions import UnauthenticatedException


_logger = logging.getLogger(__name__)

class QueryExecutor:
    """A class for executing queries."""
    def execute_query(self, access_token: str, query: str, max_tries: int = 1, **kwargs):
        """Executes a GraphQL query to the Tibber API.

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param max_tries: The amount of attempts before giving up. Set to None for infinite tries.
        :param **kwargs: Arguments to be passed in to the backoff.on_exception decorator
        """
        return asyncio.run(self.execute_async(access_token, query, max_tries, **kwargs))

    async def execute_async(self, access_token: str, query: str, max_tries: int = 1, **kwargs):
        """Coroutine for executing a GraphQL query to the Tibber API asynchronously.

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param max_tries: The amount of attempts before giving up. Set to None for infinite tries.
        :param **kwargs: Arguments to be passed in to the backoff.on_exception decorator
        """
        backoff_execution = backoff.on_exception(
            backoff.expo,
            Exception,
            max_tries = max_tries,
            max_time = 100,
            jitter = backoff.full_jitter,
            on_success = self._success_handler,
            on_backoff = self._backoff_handler,
            on_giveup = self._giveup_handler,
            **kwargs,
        )(self.execute_async_single)

        result = await backoff_execution(access_token, query)
        return result

    async def execute_async_single(self, access_token: str, query: str):
        transport = AIOHTTPTransport(
            url = API_ENDPOINT,
            headers = {"Authorization": "Bearer " + access_token},
        )

        client = gql.Client(transport=transport, fetch_schema_from_transport=True)
        try:
            result = await client.execute_async(gql.gql(query))
        except TransportQueryError as e:
            for error in e.errors:
                self._process_error(error)
        return result
    
    def _process_error(self, error):
        try:
            code = error["extensions"]["code"]
            message = error["message"]
        except KeyError:
            raise APIException(error)

        if code == "UNAUTHENTICATED":
            raise UnauthenticatedException(message)

        raise APIException(error)

    def _success_handler(self, details):
        ...

    def _backoff_handler(self, details):
        ...

    def _giveup_handler(self, details):
        ...