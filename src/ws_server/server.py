import asyncio

import websockets

from ws_server.controllers import WebSocketHandler


class WebSocketServer:
    """
    A websocket server. Receives new connections and delegates them
    to the handler.
    """

    @staticmethod
    async def start_server(host: str, port: int):
        """
        Receives a new connection via `websocket` protocol and delegates
        processing it to the `WebsocketHandler` class.
        """
        async with websockets.serve(WebSocketHandler().handle, host, port):
            await asyncio.Future()
