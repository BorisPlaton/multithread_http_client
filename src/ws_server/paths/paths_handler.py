from exceptions.server_exceptions import PathDoesNotExist
from ws_server.handlers.base import BaseHandler
from ws_server.paths.app_paths import AppPath


class PathsHandler:
    """Handles project paths."""

    def __getitem__(self, path: AppPath) -> BaseHandler:
        """
        Returns a handler of given path. If path doesn't exist
        raises an exception.
        """
        if not (handler := self.paths_data.get(path)):
            raise PathDoesNotExist
        return handler

    def __init__(self, paths_data: dict[AppPath, BaseHandler]):
        """Saves data about existing paths and their handlers."""
        self.paths_data = paths_data
