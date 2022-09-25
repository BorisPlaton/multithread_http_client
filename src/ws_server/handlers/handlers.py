from ws_server.core.structs import Request, Response
from ws_server.handlers.base import BaseHandler
from ws_server.handlers.middlewares import JSONRequestMiddleware


class HTTPClientStatusHandler(BaseHandler):
    """
    Handles the situation when status of the HTTP-client must be retrieved.
    """

    def handle(self, request: Request):
        pass


class AddNewUrlHandler(BaseHandler):
    """Handles the situation when new url is added to a download queue."""

    middlewares = [
        JSONRequestMiddleware,
    ]

    def handle(self, request: Request):
        pass
