from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    """The response which is returned by handler."""
    data: dict


@dataclass
class Request:
    """
    The abstraction of websocket connection. Represents useful data
    which may be used in handlers.
    """
    path: str
    data: Any
