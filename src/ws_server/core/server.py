import asyncio

import websockets
from websockets.legacy.server import WebSocketServerProtocol

from settings import settings
from ws_server.core.dispatcher import Dispatcher
from ws_server.paths.app_paths import AppPath


class WebSocketServer:
    """
    Checks if a new websocket connection has an existing path and runs
    a corresponding handler if it is true. Otherwise, raises an exception.
    """

    connections: set[WebSocketServerProtocol] = set()

    async def accept_new_connection(self, websocket_connection: WebSocketServerProtocol):
        """
        Adds a new websocket connection to the existing ones and
        creates a background task to retrieve new URLs.
        """
        self.connections.add(websocket_connection)
        await self.accept_messages(websocket_connection)

    async def accept_messages(self, websocket: WebSocketServerProtocol):
        """
        Accepts a new message and sends a handler's response only
        to this websocket connection.
        """
        async for message in websocket:
            handler_response = await self.request_dispatcher.dispatch_request_message(
                message, AppPath.ADD_NEW_URL
            )
            await websocket.send(handler_response)
        self.connections.remove(websocket)

    async def broadcast_url_statuses(self):
        """Broadcasts an HTTP-client status to all stored connections."""
        while True:
            await asyncio.sleep(settings.BROADCAST_TIMEOUT)
            websockets.broadcast(
                self.connections,
                await self.request_dispatcher.dispatch_request_message(
                    '{}', AppPath.LISTEN_TO_STATUS
                )
            )

    def __init__(self):
        """
        Saves a request handler which will process new websocket connections.
        """
        self.request_dispatcher = Dispatcher()
