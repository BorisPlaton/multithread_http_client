from dataclasses import dataclass

from ws_server.handlers.handlers import AddNewUrlHandler, HTTPClientStatusHandler


@dataclass
class AppPath:
    """Defines urls that are used in the application."""
    LISTEN_TO_STATUS = '/'
    ADD_NEW_URL = '/new_url'


paths = {
    AppPath.LISTEN_TO_STATUS: HTTPClientStatusHandler.setup(),
    AppPath.ADD_NEW_URL: AddNewUrlHandler.setup(),
}
