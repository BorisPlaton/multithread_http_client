from ws_server.core.structs import Request
from ws_server.handlers.base import BaseHandler
from ws_server.handlers.middlewares import ResponseMiddleware


class HTTPClientStatusHandler(BaseHandler):
    middlewares = [
        ResponseMiddleware
    ]

    def handle(self, request: Request):
        print(request)


class AddNewUrlHandler(BaseHandler):
    middlewares = [
        ResponseMiddleware
    ]

    def handle(self, request: Request):
        print(request)

