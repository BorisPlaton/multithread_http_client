import pytest

from ws_server.paths.app_paths import paths


@pytest.mark.ws_server
class TestAppPaths:

    def test_paths_variable_is_dict(self):
        assert isinstance(paths, dict)
