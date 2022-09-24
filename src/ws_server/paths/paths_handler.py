from typing import Callable

from ws_server.exceptions.external import PathDoesNotExist


class PathsHandler:
    """Handles project paths."""

    def __getitem__(self, path: str):
        """
        Returns a handler of given path. If path doesn't exist
        raises an exception.
        """
        if not (handler := self.paths_data.get(path)):
            raise PathDoesNotExist
        return handler

    def __init__(self, paths_data: dict[str, Callable]):
        """Saves data about existing paths and their handlers."""
        self.paths_data = paths_data
