from typing import Callable

from ws_server.core.structs import Request, Response


class BaseHandler:
    """The base class of request handlers."""

    middlewares = []

    def handle(self, request: Request) -> Response:
        """Handles an incoming request."""
        raise NotImplementedError("Implement a `handle` method to process a request.")

    @classmethod
    def setup(cls) -> Callable:
        """
        Sets up a handler to process a future request. Call it when
        define the handler in the path dict.
        """
        return cls._get_middleware_chain()

    @classmethod
    def _get_middleware_chain(cls) -> Callable:
        """Returns a middlewares chain. Call it to process a request."""
        chained_middleware = cls().handle
        for middleware in reversed(cls.middlewares):
            chained_middleware = middleware(chained_middleware)
        return chained_middleware
