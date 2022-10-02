import math
from typing import Iterator

from http_client.task_handling.structs import Task
from http_client.web_clients.structs import URLResourceData


class TaskScheduler:
    """Creates new tasks for workers."""

    def generate_new_tasks(self, url_data: URLResourceData) -> Iterator[Task]:
        """
        Generates new tasks with start/end byte ranges and data about
        a URL resource.
        """
        for byte_range in self.generate_byte_ranges(url_data.summary_length):
            yield Task(
                **vars(url_data),
                byte_range_start=byte_range[0],
                byte_range_end=byte_range[1],
            )

    def generate_byte_ranges(self, content_total_length: int) -> Iterator[tuple[int, int]]:
        """Generates byte-ranges of content to download."""
        yield from (
            (i * self.bytes_amount, (i + 1) * self.bytes_amount - 1)
            if (i + 1) * self.bytes_amount < content_total_length
            else (i * self.bytes_amount, content_total_length - 1)
            for i in range(math.ceil(content_total_length / self.bytes_amount))
        )

    def __init__(self, bytes_amount: int):
        """Saves a bytes amount that workers will use to download content."""
        self.bytes_amount = bytes_amount
