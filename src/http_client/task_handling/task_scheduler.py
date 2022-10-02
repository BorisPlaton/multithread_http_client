import math
from typing import Iterator

from exceptions.base import ApplicationException
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

    @property
    def bytes_amount(self):
        """Returns a bytes amount for downloading."""
        return self._bytes_amount

    @bytes_amount.setter
    def bytes_amount(self, value: int):
        """Validates that bytes amount is greater than 0 and is an integer type."""
        if not isinstance(value, int):
            raise ApplicationException("The bytes amount must be an `int` type")
        elif value <= 0:
            raise ApplicationException("The bytes amount can't be less than zero.")
        self._bytes_amount = value

    def __init__(self, bytes_amount: int = None):
        """Saves a bytes amount that workers will use to download content."""
        self._bytes_amount = None
        if bytes_amount is not None:
            self.bytes_amount = bytes_amount
