class HTTPClientSettings:
    """The settings of HTTP-client."""
    THREADS_AMOUNT = 4
    BYTES_AMOUNT = 2000
    CONTENT_DIRECTORY = 'downloaded_content'


class WebsocketServerSettings:
    """The settings of Websocket server."""
    BROADCAST_TIMEOUT = 2


class ProjectSettings(HTTPClientSettings, WebsocketServerSettings):
    """Includes settings of all project instances."""
