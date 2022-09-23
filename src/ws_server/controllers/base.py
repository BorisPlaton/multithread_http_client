from websockets.legacy.server import WebSocketServerProtocol


class BaseHandler:
    pass


class WebSocketHandler:
    """Processes websocket connections."""

    connections = set()

    async def handle(self, websocket: WebSocketServerProtocol):
        self.add_new_connection(websocket)
        async for message in websocket:
            pass

    def add_new_connection(self, websocket: WebSocketServerProtocol):
        self.connections.add(websocket)
