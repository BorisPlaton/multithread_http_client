from ws_server.handlers.handlers import AddNewUrlHandler, HTTPClientStatusHandler


paths = {
    '/': HTTPClientStatusHandler.setup(),
    '/new_url': AddNewUrlHandler.setup(),
}
