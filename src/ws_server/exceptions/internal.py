from ws_server.exceptions.base import BaseServerException


class ResponseIsNotValidType(BaseServerException):
    detail = "The handler returned response is not valid type."
