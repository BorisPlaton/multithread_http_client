from typing import NamedTuple

from aiohttp import ClientSession
from multidict import CIMultiDictProxy

from http_client.web_clients.response_validators import (
    status_code_validation, accept_ranges_validation,
    content_length_validation
)


class URLResourceData(NamedTuple):
    pass


class URLInfoReceiver:
    """Receives the data of a remote resource and validates it."""

    response_validators = [
        status_code_validation,
        content_length_validation,
        accept_ranges_validation,
    ]

    async def get_url_data_if_valid(self, url: str) -> URLResourceData:
        """
        Receives only the headers of URL and if they are valid will
        return corresponding information about the url resource.
        """
        response_headers, response_status_code = await self._get_url_info(url)
        self._validate_response(response_headers, response_status_code)
        return URLResourceData()

    async def _get_url_info(self, url: str) -> [CIMultiDictProxy, int]:
        """Returns the headers and status code of a given URL."""
        try:
            async with self.session as session:
                async with session.head(url) as response:
                    return response.headers, response.status
        finally:
            self.session.cookie_jar.clear()

    def _validate_response(self, response_headers: dict | CIMultiDictProxy, response_status_code: int):
        """
        Validates a received response via already defined validators
        in the class.
        """
        for validator in self.response_validators:
            validator(response_status_code, response_headers)

    def __init__(self):
        """Creates a client session for async requests."""
        self.session = ClientSession()
