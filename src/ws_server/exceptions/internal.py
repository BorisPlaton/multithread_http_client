from ws_server.exceptions.base import BaseServerException


class ResponseIsNotValidType(BaseServerException):

    def __init__(self, detail: str = "Controller response is not appropriate type."):
        super().__init__(detail)
