from typing import Callable


class AbstractMiddleware:
    """The abstract class of middleware."""

    def __init__(self, next_request_handler: Callable):
        """
        Saves a next request handler which will processes an incoming
        request.
        """
        self.next_request_handler = next_request_handler

    def __call__(self, request):
        """
        Processes a request and gives control to the next handler. Returns
        a response.
        """
        pass
