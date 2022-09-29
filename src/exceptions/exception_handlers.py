from typing import TypedDict

from ws_server.core.structs import Request, Response
from exceptions.base import BaseServerException


class ExceptionResponse(TypedDict):
    status: str
    message: str


class BaseExceptionHandler:
    """
    The base exception handler class in the application. Defines an
    interface which descendants must implement.
    """

    def __call__(self, exception: Exception | BaseServerException, request: Request) -> Response:
        """
        The exception handler is a callable object. All necessary operations are
        performed here to return an appropriate response.
        """
        raise NotImplementedError(
            f"You have not implemented `__call__` method in the `{self.__class__.__name__}` class."
        )


class ServerExceptionHandler(BaseExceptionHandler):
    """
    Handles server exceptions risen in the application to create
    a normal response.
    """

    def __call__(self, exception: BaseServerException, request: Request):
        """Returns a response with server exception data."""
        return Response(self.get_server_exception_info(exception))

    @staticmethod
    def get_server_exception_info(exception: BaseServerException) -> ExceptionResponse:
        """Constructs a dictionary from exception data."""
        return {"status": "error", "message": exception.detail}


class StandardExceptionHandler(BaseExceptionHandler):
    """Handles standard python exceptions occurred in the application."""

    def __call__(self, exception: Exception, request: Request):
        """Returns a response with data of standard exception."""
        return Response(data=self.get_exception_info(exception))

    @staticmethod
    def get_exception_info(exception: Exception) -> ExceptionResponse:
        """
        Returns dictionary with an exception representation.
        """
        return {"status": "error", "message": str(exception)}
