from _thread import RLock

from http_client.core.wrappers import thread_lock
from http_client.models.storages.url_workers import URLWorkersStorage


class URLWorkersRepository:
    """The repository to access a DAO with URL workers statuses."""

    _storage = URLWorkersStorage
    _lock = RLock()

    @classmethod
    @thread_lock(_lock)
    def get_workers_amount(cls, url):
        """Is thread-safe. Returns a workers amount."""
        return cls._storage.get_workers_amount(url)

    @classmethod
    @thread_lock(_lock)
    def increase_workers(cls, url):
        """Is thread-safe. Increases a workers amount."""
        return cls._storage.increase_workers(url)

    @classmethod
    @thread_lock(_lock)
    def decrease_workers(cls, url):
        """Is thread-safe. Decreases a workers amount."""
        return cls._storage.decrease_workers(url)

    @classmethod
    @thread_lock(_lock)
    def is_url_in_process(cls, url):
        """Is thread-safe. Returns is URL processing."""
        return cls._storage.is_url_in_process(url)
