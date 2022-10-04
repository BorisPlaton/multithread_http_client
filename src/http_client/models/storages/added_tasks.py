from collections import deque


class TaskQueue:
    """The task queue for background workers."""

    def push(self, element):
        """Adds a new task to the queue."""
        return self.queue.append(element)

    def pop(self):
        """
        Returns the most left task of the queue. If queue is
        empty must return none.
        """
        return self.queue.popleft() if self.is_filled else None

    @property
    def is_filled(self) -> bool:
        """Returns if the queue is empty."""
        return bool(self.queue)

    def __init__(self):
        self.queue = deque()
