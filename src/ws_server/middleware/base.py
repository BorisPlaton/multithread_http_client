from ws_server.controllers.structs import Response
from ws_server.exceptions.internal import ResponseIsNotValidType
from ws_server.middleware.abstract import AbstractMiddleware
from ws_server.paths.structs import Request


class ResponseMiddleware(AbstractMiddleware):
    """
    Checks a handler's response is an appropriate type. Otherwise, raises
    an exception.
    """

    def __call__(self, request: Request) -> Response:
        """
        Checks a controller's response is a valid type. Otherwise, an
        exception raised.
        """
        response = self.next_request_handler(request)
        if not isinstance(response, Response):
            raise ResponseIsNotValidType
        return response


class ExceptionMiddleware(AbstractMiddleware):
    """
    Catches a raised exception and creates an appropriate response.
    """

    def __call__(self, request: Request) -> Response:
        try:
            return self.next_request_handler(request)
        except:
            pass
