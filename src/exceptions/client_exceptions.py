from exceptions.base import BaseClientException


class ValidationException(BaseClientException):
    """The exception class for url validators."""
    detail = "The validation has been failed."


class ContentWasNotDownloaded(BaseClientException):
    """The exception class for url validators."""
    detail = "URL content hasn't been downloaded."
