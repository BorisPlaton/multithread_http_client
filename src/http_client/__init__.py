from http_client.core.http_client import HTTPClient
from http_client.utils.builders.builders import HTTPClientBuilder


async def start_http_client():
    http_client: HTTPClient = HTTPClientBuilder.construct()
    await http_client.start()
