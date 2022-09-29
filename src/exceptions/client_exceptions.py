from exceptions.base import BaseClientException


class ValidationException(BaseClientException):
    """The exception class for url validators."""
    detail = "The validation has been failed."
