import math
from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Task:
    """The struct defines a task unit for workers."""
    url: str
    byte_range_start: int
    byte_range_end: int

    @property
    def content_size(self):
        """Returns the total content length of task."""
        return self.byte_range_end - self.byte_range_end


class TaskScheduler:
    """Creates new tasks for workers."""

    def generate_new_tasks(self, url: str, content_size: int) -> Iterator[Task]:
        """
        Generates new tasks with start/end byte ranges and data about
        a URL resource.
        """
        for byte_range in self.generate_byte_ranges(content_size):
            yield Task(
                url,
                byte_range_start=byte_range[0],
                byte_range_end=byte_range[1],
            )

    def generate_byte_ranges(self, content_size: int) -> Iterator[tuple[int, int]]:
        """Generates byte-ranges of content to download."""
        yield from (
            (i * self.bytes_amount, (i + 1) * self.bytes_amount - 1)
            if (i + 1) * self.bytes_amount < content_size
            else (i * self.bytes_amount, content_size - 1)
            for i in range(math.ceil(content_size / self.bytes_amount))
        )

    def __init__(self, bytes_amount: int):
        """Saves a bytes amount that workers will use to download content."""
        self.bytes_amount = bytes_amount
