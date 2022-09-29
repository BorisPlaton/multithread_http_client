class HTTPClientSettings:
    """The settings of HTTP-client."""
    THREADS_AMOUNT = 4
    BYTE_RANGE = 2000


class WebsocketServerSettings:
    """The settings of Websocket server."""
    BROADCAST_TIMEOUT = 2


class ProjectSettings(HTTPClientSettings, WebsocketServerSettings):
    """Includes settings of all project instances."""
