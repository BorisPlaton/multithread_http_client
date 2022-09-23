from typing import NamedTuple, Callable


class Request(NamedTuple):
    path: str
    data: dict


class PathData(NamedTuple):
    path: str
    handler: Callable
