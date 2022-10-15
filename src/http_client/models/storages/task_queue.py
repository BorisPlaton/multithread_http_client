from collections import deque

from http_client.core.task_scheduler import Task
from http_client.utils.metaclasses import ThreadSafe


class TaskQueue(metaclass=ThreadSafe):
    """The thread-safe task queue for background workers."""

    def push(self, task: Task):
        """Adds a new task to the queue."""
        return self.queue.append(task)

    def pop(self):
        """
        Returns the most left task of the queue. If queue is
        empty must return none.
        """
        return self.queue.popleft() if self.is_filled else None

    @property
    def is_filled(self) -> bool:
        """Returns if the queue is not empty."""
        return bool(self.queue)

    def __iter__(self):
        return iter(self.queue)

    def __bool__(self):
        return bool(self.queue)

    def __init__(self):
        self.queue = deque()
