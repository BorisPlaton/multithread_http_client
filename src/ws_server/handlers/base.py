from exceptions.server_exceptions import ResponseIsNotValidType
from ws_server.core.structs import Request, Response


class BaseHandler:
    """The base class of request handlers."""

    async def handle(self, request: Request) -> Response:
        """Handles an incoming request."""
        raise NotImplementedError("Implement a `handle` method to process a request.")

    async def execute(self, request: Request):
        """Executes the handler and checks if a response is a valid type."""
        handler_response = await self.handle(request)
        if not isinstance(handler_response, Response):
            raise ResponseIsNotValidType
        return handler_response
