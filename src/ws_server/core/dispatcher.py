import json

from exceptions.base import BaseServerException
from exceptions.exception_handlers import (
    StandardExceptionHandler, ServerExceptionHandler, BaseExceptionHandler, ExceptionResponse
)
from ws_server.core.structs import Request, Response
from ws_server.paths.app_paths import paths, AppPath
from ws_server.paths.paths_handler import PathsHandler


class Dispatcher:
    """
    Dispatches an incoming request to the corresponding handler.
    """

    async def dispatch_request_message(self, message: str, path: AppPath) -> str:
        """
        Dispatches an incoming request and returns a handler's response.
        """
        handler_response = await self.get_handler_response(message, path)
        return handler_response

    async def get_handler_response(self, message: str, path: AppPath) -> str:
        """
        Gets a handler response. If some exception is raised, returns
        an exception handler's response.
        """
        try:
            request = Request(message)
            path_handler = self.existing_paths[path]
            return self.serialize_response(await path_handler.execute(request))
        except Exception as e:
            return self.serialize_response(self.process_exception(e))

    def process_exception(self, exception: Exception) -> ExceptionResponse:
        """Returns a response from the exception handler."""
        try:
            exception_handler = self.get_exception_handler(exception)
            return exception_handler(exception)
        except Exception as e:
            return self.process_exception(e)

    @staticmethod
    def serialize_response(response: Response | ExceptionResponse) -> str:
        """Serializes response to a string."""
        return json.dumps(vars(response), default=repr)

    @staticmethod
    def get_exception_handler(exception: Exception) -> BaseExceptionHandler:
        """
        The factory method that returns an appropriate exception
        handler.
        """
        return (
            ServerExceptionHandler()
            if issubclass(exception.__class__, BaseServerException)
            else StandardExceptionHandler()
        )

    def __init__(self):
        """Saves all existing paths in the project."""
        self.existing_paths = PathsHandler(paths)
