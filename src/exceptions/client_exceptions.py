from exceptions.base import BaseClientException


class ValidationException(BaseClientException):
    """The exception class for url validators."""
    detail = "The validation has been failed."


class ContentWasNotDownloaded(BaseClientException):
    """The exception class for url validators."""
    detail = "URL content hasn't been downloaded."


class URLNotInProcess(BaseClientException):
    """The exception class for url validators."""
    detail = "URL content is not processed by any worker."


class URLDoesntExist(BaseClientException):
    """The exception class for url validators."""
    detail = "URL content is already downloaded or is discarded."
