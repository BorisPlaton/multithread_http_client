from collections import deque


class BaseQueue:
    """
    The base queue. Defines an interface to interact with it and
    has base implementation.
    """

    def push(self, element):
        """Adds a new element to the queue."""
        return self.queue.append(element)

    def pop(self):
        """
        Returns the most left element of the queue. If queue is
        empty must return none.
        """
        return self.queue.popleft() if self.is_filled else None

    @property
    def is_filled(self) -> bool:
        """Returns if the queue is empty."""
        return bool(self.queue)

    def __init__(self):
        self.queue = deque()
