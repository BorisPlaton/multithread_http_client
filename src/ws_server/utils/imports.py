import importlib

import settings


def import_project_module(module_name: str):
    """Import a project module and returns data from it."""
    return importlib.import_module(settings.BASE_DIR + module_name)
