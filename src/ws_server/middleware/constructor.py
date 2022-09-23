from ws_server.middleware.abstract import AbstractMiddleware


class MiddlewareConstructor:
    """
    Creates the chain of middleware, which will process an incoming
    request and return a response.
    """

    def __init__(self, middlewares_list: list[AbstractMiddleware]):
        self.middlewares_list = middlewares_list

    def get_middleware_chain(self):
        pass
