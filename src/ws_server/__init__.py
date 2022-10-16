import asyncio

import websockets

from ws_server.core.server import WebSocketServer


async def start_websocket_server(host: str, port: int):
    """
    Receives a new connection via `websocket` protocol and delegates
    processing it to the `WebsocketHandler` class.
    """
    ws_server = WebSocketServer()
    asyncio.create_task(ws_server.broadcast_url_statuses())
    async with websockets.serve(ws_server.accept_new_connection, host, port):
        await asyncio.Future()
