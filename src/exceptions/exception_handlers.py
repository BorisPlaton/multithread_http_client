from dataclasses import dataclass
from exceptions.base import BaseServerException


@dataclass
class ExceptionResponse:
    status: str
    message: str


class BaseExceptionHandler:
    """
    The base exception handler class in the application. Defines an
    interface which descendants must implement.
    """

    def __call__(self, exception: Exception | BaseServerException) -> ExceptionResponse:
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

    def __call__(self, exception: BaseServerException):
        """Returns a response with server exception data."""
        return ExceptionResponse("error", exception.detail)


class StandardExceptionHandler(BaseExceptionHandler):
    """Handles standard python exceptions occurred in the application."""

    def __call__(self, exception: Exception):
        """Returns a response with data of standard exception."""
        return ExceptionResponse("error", str(exception))
