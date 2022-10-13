from dataclasses import dataclass
from pathlib import Path


@dataclass
class HTTPClientSettings:
    """The settings of HTTP-client."""
    THREADS_AMOUNT = 4
    BYTES_AMOUNT = 2000
    CONTENT_DIRECTORY = Path(__file__).parent.parent.parent / 'downloaded_content'


@dataclass
class WebsocketServerSettings:
    """The settings of Websocket server."""
    BROADCAST_TIMEOUT = 2


@dataclass
class ProjectSettings(HTTPClientSettings, WebsocketServerSettings):
    """Includes settings of all project instances."""
