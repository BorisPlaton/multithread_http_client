from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HTTPClientSettings:
    """The settings of HTTP-client."""
    THREADS_AMOUNT = 3
    BYTES_AMOUNT = 1000
    CONTENT_DIRECTORY = Path(__file__).parent.parent.parent / 'downloaded_content'


@dataclass(frozen=True)
class WebsocketServerSettings:
    """The settings of Websocket server."""
    BROADCAST_TIMEOUT = 3
    HOST = 'localhost'
    PORT = 8888


@dataclass(frozen=True)
class ProjectSettings(HTTPClientSettings, WebsocketServerSettings):
    """Includes settings of all project instances."""
