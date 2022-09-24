from typing import Callable

from ws_server.core.structs import Request


class BaseHandler:
    """The base class of request handlers."""

    middlewares = []

    @classmethod
    def setup(cls) -> Callable:
        """
        Sets up a handler to process a future request. Call it when
        define the handler in a path dict.
        """
        return cls._get_middleware_chain()

    def handle(self, request: Request):
        """Handles an incoming request."""
        raise NotImplementedError("Implement a `handle` method to process a request.")

    @classmethod
    def _get_middleware_chain(cls) -> Callable:
        chained_middleware = cls().handle
        for middleware in reversed(cls.middlewares):
            chained_middleware = middleware(chained_middleware)
        return chained_middleware
