from typing import NamedTuple, Any

from aiohttp import ClientSession
from multidict import CIMultiDictProxy

from exceptions.base import ApplicationException
from http_client.web_clients.response_validators import (
    status_code_validation, accept_ranges_validation,
    content_length_validation
)


class URLResourceData(NamedTuple):
    content_length: int


class HeaderData(NamedTuple):
    name: str
    value_type: Any


class URLInfoReceiver:
    """Receives the data of a remote resource and validates it."""

    response_validators = [
        status_code_validation,
        content_length_validation,
        accept_ranges_validation,
    ]

    headers_to_return = {
        'content_length': HeaderData('Content-Length', int),
    }

    async def get_url_data_if_valid(self, url: str) -> URLResourceData:
        """
        Receives only the headers of URL and if they are valid will
        return corresponding information about the url resource.
        """
        response_headers, response_status_code = await self._get_url_info(url)
        self._validate_response(response_headers, response_status_code)
        resource_data = self._get_resource_necessary_headers_values(response_headers)
        return URLResourceData(*resource_data)

    @classmethod
    def _get_resource_necessary_headers_values(cls, headers: dict | CIMultiDictProxy) -> dict:
        """Returns all necessary headers and their values in a dictionary."""
        try:
            return {
                value_name: header_info.value_type(headers[header_info.name])
                for value_name, header_info in cls.headers_to_return.items()
            }
        except (ValueError, KeyError):
            raise ApplicationException("Can't construct a dictionary with all necessary headers.")

    @staticmethod
    async def _get_url_info(url: str) -> [CIMultiDictProxy, int]:
        """Returns the headers and status code of a given URL."""
        async with ClientSession() as session:
            async with session.head(url) as response:
                return response.headers, response.status

    def _validate_response(self, response_headers: dict | CIMultiDictProxy, response_status_code: int):
        """
        Validates a received response via already defined validators
        in the class.
        """
        for validator in self.response_validators:
            validator(response_status_code, response_headers)
