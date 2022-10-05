from collections import deque
from threading import RLock

from http_client.core.utils import instance_thread_lock
from http_client.task_handling.structs import Task


class TaskQueue:
    """The task queue for background workers."""

    @instance_thread_lock('lock')
    def push(self, task: Task):
        """Adds a new task to the queue."""
        return self.queue.append(task)

    @instance_thread_lock('lock')
    def pop(self):
        """
        Returns the most left task of the queue. If queue is
        empty must return none.
        """
        return self.queue.popleft() if self.is_filled else None

    @property
    @instance_thread_lock('lock')
    def is_filled(self) -> bool:
        """Returns if the queue is not empty."""
        return bool(self.queue)

    def __init__(self):
        self.queue = deque()
        self.lock = RLock()
