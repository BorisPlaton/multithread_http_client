import requests
from requests import Response

from exceptions.client_exceptions import ValidationException, ContentWasNotDownloaded
from http_client.web_clients.mixins import ResponseValidator
from http_client.web_clients.response_validators import status_code_validation


class URLContentDownloader(ResponseValidator):
    """Downloads content from given URL."""

    response_validators = [
        status_code_validation
    ]

    def get_url_content(
            self, url: str, encoding: str, byte_range_start: int, byte_range_end: int
    ) -> bytes | None:
        """Downloads the content of URL if it passes all validations."""
        try:
            response = self.send_request(url, encoding, byte_range_start, byte_range_end)
            self.validate_response(response.headers, response.status_code)
            return response.content
        except ValidationException:
            raise ContentWasNotDownloaded

    def send_request(self, url: str, encoding: str, byte_range_start: int, byte_range_end: int) -> Response:
        """Sends a request and returns a response."""
        request_headers = self.construct_request_headers(encoding, byte_range_start, byte_range_end)
        return requests.get(url, headers=request_headers)

    @staticmethod
    def construct_request_headers(encoding: str, byte_range_start, byte_range_end) -> dict:
        """Constructs headers for sending a request."""
        return {
            'Accept-Encoding': encoding,
            'Range': f'bytes={byte_range_start}-{byte_range_end}',
        }
