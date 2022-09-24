from ws_server.exceptions.external import PathDoesNotExist
from ws_server.utils.imports import import_module


class PathsHandler:
    """Handles project paths."""

    @staticmethod
    def get_paths_data(module_with_urls: str, paths_variable_name: str) -> dict:
        """Returns a dict which contains data about paths and their handlers."""
        paths_module = import_module(module_with_urls)
        if (paths_variable := getattr(paths_module, paths_variable_name)) is None:
            raise ValueError(
                f"You haven't specified a `{paths_variable_name}` in the {module_with_urls} module."
            )
        elif not isinstance(paths_variable, dict):
            raise ValueError(
                f"The `{paths_variable_name}` variable must be a dictionary."
            )
        return paths_variable

    def __getitem__(self, path: str):
        """
        Returns a handler of given path. If path doesn't exist
        raises an exception.
        """
        if not (handler := self.routes_data.get(path)):
            raise PathDoesNotExist
        return handler

    def __init__(self, module_with_paths: str, paths_variable: str):
        """Saves data about existing paths and their handlers."""
        self.routes_data = self.get_paths_data(module_with_paths, paths_variable)
