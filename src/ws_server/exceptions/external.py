from ws_server.exceptions.base import BaseServerException


class PathDoesNotExist(BaseServerException):
    detail = "The provided url doesn't exist."
