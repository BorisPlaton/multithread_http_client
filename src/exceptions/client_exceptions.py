from exceptions.base import BaseClientException


class ValidationException(BaseClientException):
    """The exception class for url validators."""
    detail = "The validation has been failed."


class ContentWasNotDownloaded(BaseClientException):
    """The exception class for url validators."""
    detail = "URL content hasn't been downloaded."


class URLDataException(BaseClientException):
    """The exception class for url validators."""
    detail = "Exception is risen due to the status of URL."


class URLDoesntExist(BaseClientException):
    """The exception class for url validators."""
    detail = "URL doesn't exist."
