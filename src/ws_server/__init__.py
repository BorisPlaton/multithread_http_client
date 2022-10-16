import asyncio

import websockets

from settings import settings
from ws_server.core.server import WebSocketServer


async def start_websocket_server():
    """
    Receives a new connection via `websocket` protocol and delegates
    processing it to the `WebsocketHandler` class.
    """
    ws_server = WebSocketServer()
    asyncio.create_task(ws_server.broadcast_url_statuses())
    async with websockets.serve(ws_server.accept_new_connection, settings.HOST, settings.PORT):
        await asyncio.Future()
