import asyncio

import websockets

from ws_server.core.server import WebSocketServer


async def start_server(host: str, port: int):
    """
    Receives a new connection via `websocket` protocol and delegates
    processing it to the `WebsocketHandler` class.
    """
    async with websockets.serve(WebSocketServer().handle, host, port):
        await asyncio.Future()
