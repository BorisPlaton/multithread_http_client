import importlib
from types import ModuleType


def import_module(module_name: str) -> ModuleType:
    """Import a project module and returns data from it."""
    return importlib.import_module(module_name)
