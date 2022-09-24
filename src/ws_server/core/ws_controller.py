from websockets.legacy.server import WebSocketServerProtocol

from ws_server.core.dispatcher import Dispatcher
from ws_server.core.structs import Request


class WebSocketHandler:
    """
    Checks if a new websocket connection has an existing path and runs
    a corresponding handler if it is true. Otherwise, raises an exception.
    """

    connections = set()

    async def handle(self, websocket: WebSocketServerProtocol):
        """
        Handles a websocket connection. Actually, it constructs a `Request`
        instance and runs a request handler to process a new message from the
        existing connection.
        """
        self.add_new_connection(websocket)
        async for message in websocket:
            self.request_dispatcher(self.construct_request(websocket, message))

    @classmethod
    def add_new_connection(cls, websocket_connection: WebSocketServerProtocol):
        """Adds a new websocket connection to the existing ones."""
        cls.connections.add(websocket_connection)

    @staticmethod
    def construct_request(websocket: WebSocketServerProtocol, message) -> Request:
        """
        Construct an abstraction `Request` from a websocket connection with
        it message.
        """
        return Request(
            path=websocket.path,
            data=message
        )

    def __init__(self):
        """Saves a request handler which will process new websocket connections."""
        self.request_dispatcher = Dispatcher()
