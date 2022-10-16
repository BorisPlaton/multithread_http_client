import pytest

from ws_server.core.structs import Request
from ws_server.handlers.base import BaseHandler


@pytest.mark.ws_server
class TestBaseHandler:

    @pytest.fixture
    def base_handler(self):
        return BaseHandler()

    @pytest.mark.asyncio
    async def test_handle_method_raises_exception(self, base_handler):
        with pytest.raises(NotImplementedError):
            await base_handler.handle(Request(raw_data='{"hello": "world"}'))
