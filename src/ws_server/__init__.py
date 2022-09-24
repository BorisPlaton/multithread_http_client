import asyncio

import websockets

from ws_server.core.base import WebSocketHandler


async def start_server(host: str, port: int):
    """
    Receives a new connection via `websocket` protocol and delegates
    processing it to the `WebsocketHandler` class.
    """
    async with websockets.serve(WebSocketHandler().handle, host, port):
        await asyncio.Future()
