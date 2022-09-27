from collections import deque

from http_client.data_storage.data_collections.abstract import AbstractCollection


class SetCollection(AbstractCollection):
    """The collection that is implemented over a `set` class."""

    def add(self, item):
        return self.source_data_structure.add(item)

    def remove(self, item):
        return self.source_data_structure.remove(item)

    @property
    def is_empty(self) -> bool:
        return not bool(self.source_data_structure)

    def __iter__(self):
        return iter(self.source_data_structure)

    def __init__(self):
        self.source_data_structure = set()


class QueueCollection(AbstractCollection):
    """The collection that is implemented over a `collections.deque` class."""

    def add(self, item):
        return self.source_data_structure.append(item)

    def remove(self, item):
        return self.source_data_structure.remove(item)

    @property
    def is_empty(self) -> bool:
        return not bool(self.source_data_structure)

    def get(self):
        return self.source_data_structure[0] if not self.is_empty else None

    def pop(self):
        return self.source_data_structure.popleft() if not self.is_empty else None

    def __iter__(self):
        return iter(self.source_data_structure)

    def __init__(self):
        self.source_data_structure = deque()
