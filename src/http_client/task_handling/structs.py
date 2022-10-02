from dataclasses import dataclass

from http_client.web_clients.structs import URLResourceData


@dataclass
class Task(URLResourceData):
    """The struct defines a task unit for workers."""
    byte_range_start: int
    byte_range_end: int
