class AbstractCollection:
    """Defines an interface to interact with a collection of data."""

    def add(self, *args, **kwargs):
        """Adds a new item to the collection."""
        raise NotImplementedError

    def remove(self, *args, **kwargs):
        """Removes a specific item from the collection."""
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        """Shows if a collection is empty."""
        raise NotImplementedError

    def __iter__(self):
        """The collection must be iterable."""
        raise NotImplementedError

    def __repr__(self):
        """Shows the list of collection elements."""
        return f"{list(self)}"
