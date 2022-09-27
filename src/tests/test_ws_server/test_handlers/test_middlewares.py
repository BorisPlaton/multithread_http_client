import pytest

from ws_server.core.structs import Request
from ws_server.exceptions.external import RequestDataIsNotJSON
from ws_server.handlers.middlewares import BaseMiddleware, JSONRequestMiddleware


@pytest.mark.ws_server
class TestBaseMiddleware:

    @pytest.fixture
    def base_middleware(self):
        return BaseMiddleware(lambda x: x)

    def test_exception_raised_on_call_method(self, base_middleware):
        with pytest.raises(NotImplementedError):
            base_middleware(Request(data='2', path='/'))


@pytest.mark.ws_server
class TestJSONRequestMiddleware:

    @pytest.fixture
    def json_request_middleware(self):
        return JSONRequestMiddleware(lambda x: x)

    def test_successful_deserialization(self, json_request_middleware):
        json_in_string = """{"hello": "world"}"""
        assert isinstance(json_request_middleware.deserialize_request_data_to_json(json_in_string), dict)

    def test_deserialization_raises_server_exception_on_failure(self, json_request_middleware):
        test_parameters = ["{'g':1}", 1, dict, "", "423141"]
        for parameter in test_parameters:
            with pytest.raises(RequestDataIsNotJSON):
                json_request_middleware.deserialize_request_data_to_json(parameter)

    def test_middleware_change_string_json_to_dict(self, json_request_middleware):
        test_request = Request('/', """{"hello": "world"}""")
        changed_request = json_request_middleware(test_request)
        assert changed_request is test_request
        assert isinstance(changed_request.data, dict)
