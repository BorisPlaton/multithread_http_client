from ws_server.controllers.base import BaseHandler
from ws_server.paths.structs import PathData


class RequestHandler:
    """
    Checks an incoming request has an existing path and gives the request
    to the corresponding handler. Otherwise, raises an exception.
    """

    def get_existing_paths(self) -> list[str]:
        pass

    def get_existing_handlers(self) -> list[BaseHandler]:
        pass

    def _get_project_routes(self, routers_list_path: str) -> list[PathData]:
        pass

    def __init__(self):
        self.existing_paths = self.get_existing_paths()

    def __call__(self, request):
        pass
