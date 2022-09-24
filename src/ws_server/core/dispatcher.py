from ws_server.core.structs import Request, Response
from ws_server.paths.app_paths import paths
from ws_server.paths.paths_handler import PathsHandler


class Dispatcher:
    """
    Dispatches an incoming request to the corresponding handler.
    """

    def dispatch_request(self, request: Request):
        """
        Dispatches an incoming request and returns a handler's response.
        """
        try:
            path_handler = self.existing_paths[request.path]
            handler_response = path_handler(request)
        except Exception as e:
            handler_response = self.handle_exception(e)
        return self.serialize_response(handler_response)

    def handle_exception(self, exception: Exception) -> Response:
        """
        If any exception occurs in the application it will handle it and will
        return an appropriate response.
        """

    def serialize_response(self, response: Response) -> str:
        """Serializes a handler's response to string."""

    def __init__(self):
        """Saves all existing paths in the project."""
        self.existing_paths = PathsHandler(paths)
