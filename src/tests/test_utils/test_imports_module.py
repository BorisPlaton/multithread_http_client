import pytest

from ws_server.utils.imports import import_project_module


def test_import_project_module_is_working_with_strings():
    module_name = 'tests.test_utils.source.module_for_test'
    imported_module = import_project_module(module_name)
    assert imported_module.IMPORTANT_CONSTANT == 1
