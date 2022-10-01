from typing import NamedTuple, Any

from aiohttp import ClientSession
from multidict import CIMultiDictProxy

from exceptions.base import ApplicationException
from http_client.web_clients.response_validators import (
    status_code_validation, accept_ranges_validation,
    content_length_validation, content_encoding_validation
)
from http_client.web_clients.structs import URLResourceData


class HeaderData(NamedTuple):
    header_name: str
    value_type: Any


class URLInfoReceiver:
    """Receives the data of a remote resource and validates it."""

    response_validators = [
        status_code_validation,
        accept_ranges_validation,
        content_encoding_validation,
        content_length_validation,
    ]

    headers_to_return = {
        'summary_length': HeaderData('Content-Length', int),
        'encoding_type': HeaderData('Content-Encoding', str),
    }

    async def get_url_data_if_valid(self, url: str) -> URLResourceData:
        """
        Receives only the headers of request to URL and if they are
        valid will return corresponding information about the URL
        resource.
        """
        response_headers, response_status_code = await self.make_request(url)
        self.validate_response(response_headers, response_status_code)
        resource_data = self.get_necessary_resource_headers_values(response_headers)
        return URLResourceData(**resource_data, url=url)

    async def make_request(self, url: str) -> [CIMultiDictProxy, int]:
        """Returns the headers and the status code of a request to URL."""
        async with ClientSession() as session:
            async with session.head(url, headers=self.get_request_headers()) as response:
                return response.headers, response.status

    def validate_response(self, response_headers: dict | CIMultiDictProxy, response_status_code: int):
        """
        Validates a received response via already defined validators
        in the class.
        """
        for validator in self.response_validators:
            validator(response_status_code, response_headers)

    @staticmethod
    def get_request_headers() -> dict:
        """
        Returns a dictionary with request headers. It is used to receive
        information about a remote resource.
        """
        return {
            'Accept-Encoding': 'gzip, deflate'
        }

    @classmethod
    def get_necessary_resource_headers_values(cls, headers: dict | CIMultiDictProxy) -> dict:
        """Returns all necessary headers and their values in a dictionary."""
        try:
            return {
                value_name: header_info.value_type(headers[header_info.header_name])
                for value_name, header_info in cls.headers_to_return.items()
            }
        except (ValueError, KeyError):
            raise ApplicationException("Can't construct a dictionary with all necessary headers.")
