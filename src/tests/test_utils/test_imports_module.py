from ws_server.utils.imports import import_module


def test_import_project_module_is_working_with_string():
    module_name = 'tests.test_utils.source.module_for_test'
    imported_module = import_module(module_name)
    assert imported_module.IMPORTANT_CONSTANT == 1
