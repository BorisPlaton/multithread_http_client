from typing import NamedTuple


class Task(NamedTuple):
    """The struct defines a task unit for workers."""
    url_to_download: str
    byte_range_start: int
    byte_range_end: int
    summary_length: int
