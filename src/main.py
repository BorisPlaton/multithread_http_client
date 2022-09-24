import asyncio

from ws_server import start_server


async def main(host: str, port: int):
    """Entry point to the program. Starts a websocket server."""
    await start_server(host, port)


if __name__ == '__main__':
    asyncio.run(main('localhost', 8888))
