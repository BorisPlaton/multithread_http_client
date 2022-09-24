from ws_server.core.structs import Response
from ws_server.exceptions.internal import ResponseIsNotValidType


class ResponseMiddleware:

    def __init__(self, next_handler):
        self.next_handler = next_handler

    def __call__(self, request):
        response = self.next_handler(request)
        if not isinstance(response, Response):
            raise ResponseIsNotValidType
        return response
