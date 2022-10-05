from dataclasses import dataclass

from http_client.web_clients.structs import URLResourceData


@dataclass(frozen=True)
class Task(URLResourceData):
    """The struct defines a task unit for workers."""
    byte_range_start: int
    byte_range_end: int

    @property
    def content_size(self):
        """Returns the total content length of task."""
        return self.byte_range_end - self.byte_range_end
