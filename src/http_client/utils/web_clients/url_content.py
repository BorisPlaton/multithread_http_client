import requests
from requests import Response

from exceptions.client_exceptions import ValidationException, ContentWasNotDownloaded
from http_client.utils.web_clients.mixins import ResponseValidator
from http_client.utils.web_clients.response_validators import status_code_validation


class URLContentDownloader(ResponseValidator):
    """Downloads content from given URL."""

    response_validators = [
        status_code_validation
    ]

    @classmethod
    def get_url_content(
            cls, url: str, byte_range_start: int, byte_range_end: int
    ) -> bytes:
        """Downloads the content of URL if it passes all validations."""
        try:
            response = cls.send_request(url, byte_range_start, byte_range_end)
            cls.validate_response(response.headers, response.status_code)
            return response.content
        except ValidationException as e:
            raise ContentWasNotDownloaded(e.detail)
        except Exception as e:
            raise ContentWasNotDownloaded(str(e))

    @classmethod
    def send_request(cls, url: str, byte_range_start: int, byte_range_end: int) -> Response:
        """Sends a request and returns a response."""
        request_headers = cls.construct_request_headers(byte_range_start, byte_range_end)
        return requests.get(url, headers=request_headers)

    @staticmethod
    def construct_request_headers(byte_range_start, byte_range_end) -> dict:
        """Constructs headers for sending a request."""
        return {
            'Range': f'bytes={byte_range_start}-{byte_range_end}',
        }
