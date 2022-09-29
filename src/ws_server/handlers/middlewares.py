import json
from json import JSONDecodeError

from exceptions.server_exceptions import RequestDataIsNotJSON
from ws_server.core.structs import Response, Request


class BaseMiddleware:
    """The base middleware class."""

    def __init__(self, next_handler):
        """Accepts a next middleware or a handler."""
        self.next_handler = next_handler

    def __call__(self, request: Request) -> Response:
        """The middleware instance will be called to perform operations."""
        raise NotImplementedError(
            f"`{self.__class__.__name__}` has not implemented a `__call__` method."
        )


class JSONRequestMiddleware(BaseMiddleware):
    """Deserializes incoming request data to the dictionary."""

    def __call__(self, request):
        """
        Deserializes a request data from string to dict and set
        it to the `request.data` field.
        """
        deserialized_data = self.deserialize_request_data_to_json(request.data)
        request.data = deserialized_data
        response = self.next_handler(request)
        return response

    @staticmethod
    def deserialize_request_data_to_json(request_data: str) -> dict:
        """Performs a deserialization operation from string to dictionary."""
        try:
            deserialized_data = json.loads(request_data)
        except (JSONDecodeError, TypeError):
            raise RequestDataIsNotJSON
        if not isinstance(deserialized_data, dict):
            raise RequestDataIsNotJSON
        return deserialized_data
