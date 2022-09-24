import settings
from ws_server.core.structs import Request
from ws_server.paths.paths_handler import PathsHandler


class Dispatcher:
    """Dispatches an incoming request. Passes it """

    def __call__(self, request: Request):
        """
        Dispatches an incoming request and returns a handler's response.
        """
        path_handler = self.existing_paths[request.path]
        return path_handler(request)

    def __init__(self):
        """Saves all existing paths in the project."""
        self.existing_paths = PathsHandler(settings.URLS_MODULE, settings.URLS_VARIABLE)
