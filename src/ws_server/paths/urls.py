from ws_server.controllers.handlers import AddNewUrlHandler, HTTPClientStatusHandler
from ws_server.paths.structs import PathData


routes = [
    PathData('/new_url', AddNewUrlHandler),
    PathData('/', HTTPClientStatusHandler),
]
