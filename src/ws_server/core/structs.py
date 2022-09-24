from typing import NamedTuple, Any


class Response(NamedTuple):
    """The response which is returned by handler."""
    data: dict


class Request(NamedTuple):
    """
    The abstraction of websocket connection. Represents useful data
    which may be used in handlers.
    """
    path: str
    data: Any
