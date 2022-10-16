import asyncio

from http_client import start_http_client
from ws_server import start_websocket_server


async def main(host: str, port: int):
    """Entry point to the program. Starts a websocket server."""
    await asyncio.gather(
        start_http_client(), start_websocket_server(host, port)
    )


if __name__ == '__main__':
    asyncio.run(main('localhost', 8888))
