from exceptions.base import BaseServerException


class PathDoesNotExist(BaseServerException):
    detail = "The provided url doesn't exist."


class RequestDataIsNotJSON(BaseServerException):
    detail = "You must to specify request data in JSON format."


class ResponseIsNotValidType(BaseServerException):
    detail = "The handler returned response is not valid type."
