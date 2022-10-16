from exceptions.base import BaseServerException


class PathDoesNotExist(BaseServerException):
    detail = "The provided url doesn't exist."


class WrongRequestData(BaseServerException):
    detail = "The request data is wrong."


class ResponseIsNotValidType(BaseServerException):
    detail = "The handler returned response is not valid type."
