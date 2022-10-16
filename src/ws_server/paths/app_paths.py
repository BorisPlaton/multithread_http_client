from enum import auto, Enum

from ws_server.handlers.handlers import AddNewUrlHandler, HTTPClientStatusHandler


class AppPath(Enum):
    """Defines urls that are used in the application."""
    LISTEN_TO_STATUS = auto()
    ADD_NEW_URL = auto()


paths = {
    AppPath.LISTEN_TO_STATUS: HTTPClientStatusHandler(),
    AppPath.ADD_NEW_URL: AddNewUrlHandler(),
}
