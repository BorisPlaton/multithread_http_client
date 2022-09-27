import pytest

from ws_server.core.structs import Request
from ws_server.handlers.base import BaseHandler


@pytest.mark.ws_server
class TestBaseHandler:

    @pytest.fixture
    def base_handler(self):
        return BaseHandler()

    @pytest.fixture
    def request_(self):
        return Request(path='/', data={'hello': 'world'})

    def test_handle_method_raises_exception(self, base_handler, request_):
        with pytest.raises(NotImplementedError):
            base_handler.handle(request_)

    def test_constructing_middleware_chain_with_empty_middlewares_list(self, base_handler):
        chained_middleware = base_handler._get_middleware_chain()
        assert chained_middleware.__name__ == base_handler.handle.__name__

    def test_constructing_middleware_chain_with_filled_middlewares_list(self, base_handler):
        class FakeMiddleware:

            def __init__(self, next_fake_middleware):
                self.next_handler = next_fake_middleware

        class FakeMiddleware2:

            def __init__(self, next_fake_middleware):
                self.next_handler = next_fake_middleware

        middlewares_list = [FakeMiddleware, FakeMiddleware2]
        base_handler.__class__.middlewares = middlewares_list
        middleware_chain = base_handler._get_middleware_chain()

        for i in range(3):
            if i == 0:
                assert isinstance(middleware_chain, FakeMiddleware)
                middleware_chain = middleware_chain.next_handler
            elif i == 1:
                assert isinstance(middleware_chain, FakeMiddleware2)
                middleware_chain = middleware_chain.next_handler
            else:
                assert middleware_chain.__name__ == base_handler.handle.__name__

    def test_setup_method_return_callable(self, base_handler):
        assert callable(base_handler.setup)
