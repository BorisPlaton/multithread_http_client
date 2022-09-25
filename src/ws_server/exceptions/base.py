class BaseServerException(Exception):
    """The base server exception."""
    detail = "The unknown exception occurred."

    def __init__(self, exception_detail: str = None):
        self.detail = exception_detail or self.detail
