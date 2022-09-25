from typing import Callable

from ws_server.core.structs import Request, Response
from ws_server.exceptions.internal import ResponseIsNotValidType
from ws_server.handlers.middlewares import BaseMiddleware


class BaseHandler:
    """The base class of request handlers."""

    middlewares: list[type[BaseMiddleware]] = []

    def handle(self, request: Request) -> Response:
        """Handles an incoming request."""
        raise NotImplementedError("Implement a `handle` method to process a request.")

    @classmethod
    def setup(cls) -> Callable:
        """
        Sets up a handler to process a future request. Call it when
        define the handler in the path dict.
        """
        middleware_chain = cls._get_middleware_chain()

        def execute_handler(request: Request):
            """Executes the handler and checks if a response is a valid type."""
            handler_response = middleware_chain(request)
            if not isinstance(handler_response, Response):
                raise ResponseIsNotValidType
            return handler_response

        return execute_handler

    @classmethod
    def _get_middleware_chain(cls) -> Callable:
        """Returns a middlewares chain. Call it to process a request."""
        chained_middleware = cls().handle
        for middleware in reversed(cls.middlewares):
            chained_middleware = middleware(chained_middleware)
        return chained_middleware
