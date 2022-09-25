import asyncio
from typing import Coroutine

import websockets
from websockets.legacy.server import WebSocketServerProtocol

import settings
from ws_server.core.dispatcher import Dispatcher
from ws_server.core.structs import Request


class WebSocketHandler:
    """
    Checks if a new websocket connection has an existing path and runs
    a corresponding handler if it is true. Otherwise, raises an exception.
    """

    connections: set[WebSocketServerProtocol] = set()

    async def handle(self, websocket: WebSocketServerProtocol):
        """
        Handles a websocket connection. Actually, it constructs a `Request`
        instance and runs a request handler to process a new message from the
        existing connection.
        """
        self.add_new_connection(websocket)
        await asyncio.gather(*self.create_new_connection_coroutines(websocket))

    @classmethod
    def add_new_connection(cls, websocket_connection: WebSocketServerProtocol):
        """Adds a new websocket connection to the existing ones."""
        cls.connections.add(websocket_connection)

    def create_new_connection_coroutines(self, websocket) -> list[Coroutine]:
        """
        Returns a list of coroutines for a new connection. Depending on
        how many connections there are already it may or may not include
        a broadcast coroutine.
        """
        coroutines_list = [self.accept_new_messages(websocket)]
        if len(self.connections) == 1:
            coroutines_list.append(self.broadcast_response())
        return coroutines_list

    async def accept_new_messages(self, websocket: WebSocketServerProtocol):
        """
        Accepts a new message and sends a handler's response only
        to this websocket connection.
        """
        async for message in websocket:
            request = self.construct_request(websocket, message)
            handler_response = self.request_dispatcher.dispatch_request(request)
            await websocket.send(handler_response)
        else:
            self.connections.remove(websocket)

    async def broadcast_response(self):
        """Broadcasts an HTTP-client status to all saved connections."""
        while True:
            await asyncio.sleep(settings.BROADCAST_TIMEOUT)
            websockets.broadcast(self.connections, 'hello')

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
        """
        Saves a request handler which will process new websocket connections.
        """
        self.request_dispatcher = Dispatcher()
