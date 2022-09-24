from ws_server.core.structs import Request
from ws_server.handlers.base import BaseHandler
from ws_server.handlers.middlewares import ResponseMiddleware


class HTTPClientStatusHandler(BaseHandler):
    """
    Handles the situation when status of the HTTP-client must be retrieved.
    """

    middlewares = [
        ResponseMiddleware
    ]

    def handle(self, request: Request):
        pass


class AddNewUrlHandler(BaseHandler):
    """Handles the situation when new url is added to a download queue."""

    middlewares = [
        ResponseMiddleware
    ]

    def handle(self, request: Request):
        pass
