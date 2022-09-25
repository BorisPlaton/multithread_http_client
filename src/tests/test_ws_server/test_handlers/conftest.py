import pytest

from ws_server.core.structs import Request
from ws_server.handlers.base import BaseHandler
from ws_server.handlers.middlewares import JSONRequestMiddleware


@pytest.fixture
def base_handler():
    return BaseHandler()


@pytest.fixture
def request_():
    return Request(path='/', data={'hello': 'world'})


@pytest.fixture
def json_request_middleware():
    return JSONRequestMiddleware(lambda x: x)
