import asyncio

from ws_server.server import WebSocketServer


async def main(host: str, port: int):
    """Entry point to the program."""
    await WebSocketServer.start_server(host, port)


if __name__ == '__main__':
    asyncio.run(main('localhost', 8888))
