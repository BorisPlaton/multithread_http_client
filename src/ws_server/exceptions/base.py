class BaseServerException(Exception):
    """The base server exception."""

    def __init__(self, detail: str = "Exception occurred."):
        self.detail = detail
