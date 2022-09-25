import pytest

from ws_server.exceptions.external import PathDoesNotExist
from ws_server.paths.paths_handler import PathsHandler


@pytest.mark.ws_server
class TestPathsHandler:

    def test_paths_handler_initialization_accepts_dict_arg(self):
        handler = PathsHandler(
            {'2': int},
        )
        assert isinstance(handler.paths_data, dict)

    def test_paths_handler_is_subscriptable(self):
        handler = PathsHandler(
            {'2': int},
        )
        assert handler['2'] == int

    def test_paths_handler_raises_error_if_item_doesnt_exist(self):
        handler = PathsHandler(
            {'2': int},
        )
        with pytest.raises(PathDoesNotExist):
            handler['3']
