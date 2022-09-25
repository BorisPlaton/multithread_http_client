import json

from ws_server.core.structs import Request, Response
from ws_server.exceptions.base import BaseServerException
from ws_server.exceptions.exception_handlers import (
    ServerExceptionHandler, BaseExceptionHandler, StandardExceptionHandler
)
from ws_server.paths.app_paths import paths
from ws_server.paths.paths_handler import PathsHandler


class Dispatcher:
    """
    Dispatches an incoming request to the corresponding handler.
    """

    def dispatch_request(self, request: Request):
        """
        Dispatches an incoming request and returns a handler's response.
        """
        try:
            path_handler = self.existing_paths[request.path]
            handler_response = path_handler(request)
        except Exception as e:
            exception_handler = self.get_exception_handler(e)
            handler_response = exception_handler(e, request)
        return self.serialize_response(handler_response)

    @staticmethod
    def serialize_response(response: Response) -> str:
        """Serializes a handler's response to string."""
        response_data_in_string = json.dumps(response.data)
        return response_data_in_string

    @staticmethod
    def get_exception_handler(exception: Exception) -> BaseExceptionHandler:
        """
        The factory method that returns an appropriate exception handler
        to process an occurred exception.
        """
        if issubclass(exception.__class__, BaseServerException):
            return ServerExceptionHandler()
        return StandardExceptionHandler()

    def __init__(self):
        """Saves all existing paths in the project."""
        self.existing_paths = PathsHandler(paths)
