from typing import NamedTuple, Any

from aiohttp import ClientSession
from multidict import CIMultiDictProxy

from exceptions.base import ApplicationException
from http_client.web_clients.mixins import ResponseValidator
from http_client.web_clients.response_validators import (
    status_code_validation, accept_ranges_validation,
    content_length_validation
)
from http_client.web_clients.structs import URLResourceData


class HeaderData(NamedTuple):
    header_name: str
    value_type: Any


class URLInfoReceiver(ResponseValidator):
    """Receives the data of a remote resource and validates it."""

    response_validators = [
        status_code_validation,
        accept_ranges_validation,
        content_length_validation,
    ]

    headers_to_return = {
        'summary_length': HeaderData('Content-Length', int),
    }

    async def get_url_data_if_valid(self, url: str) -> URLResourceData:
        """
        Receives only the headers of request to URL and if they are
        valid will return corresponding information about the URL
        resource.
        """
        response_headers, response_status_code = await self.send_request(url)
        self.validate_response(response_headers, response_status_code)
        resource_data = self.get_necessary_resource_headers_values(response_headers)
        return URLResourceData(**resource_data, url=url)

    @staticmethod
    async def send_request(url: str) -> [CIMultiDictProxy, int]:
        """Returns the headers and the status code of a request to URL."""
        async with ClientSession() as session:
            async with session.head(url) as response:
                return response.headers, response.status

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
