class ApplicationException(Exception):
    """
    The exception class placed at the top of an application exceptions hierarchy.
    """
    detail = "The application exception"

    def __init__(self, exception_detail: str = None):
        self.detail = exception_detail or self.detail


class BaseServerException(ApplicationException):
    """The base server exception."""
    detail = "The unknown websocket server exception occurred."


class BaseClientException(ApplicationException):
    detail = "The unknown HTTP-client exception occurred."
