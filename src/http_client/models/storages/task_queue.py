from collections import deque
from threading import RLock

from http_client.core.task_scheduler import Task
from http_client.utils.wrappers import instance_thread_lock


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
