from threading import RLock

from http_client.core.utils import thread_lock
from http_client.models.storages.srtucts import (
    BaseURLData, DiscardedURL,
    InProcessURLData
)
from http_client.models.storages.url_statuses import URLStatusesStorage


class URLStatusesRepository:
    """
    The repository to interact with a URL storage. Has additional
    methods.
    """

    _storage = URLStatusesStorage
    _lock = RLock()

    @classmethod
    @thread_lock(_lock)
    def add_url(cls, url: BaseURLData):
        """Adds new URL data to the storage."""
        return cls._storage.add_url(url)

    @classmethod
    @thread_lock(_lock)
    def update_url_data(cls, url: str, **kwargs) -> bool:
        """Adds new URL data to the storage."""
        if not (old_url_data := cls._storage.pop_url(url)):
            return False
        url_data_fields = vars(old_url_data)
        url_data_fields.update({**kwargs})
        new_url_data = old_url_data.__class__(**url_data_fields)
        cls.add_url(new_url_data)
        return True

    @classmethod
    @thread_lock(_lock)
    def pop_url(cls, url: str):
        """
        Decreases the quantity of URL workers. If after decrease
        workers amount is 0, deletes it from observing.
        """
        return cls._storage.pop_url(url)

    @classmethod
    @thread_lock(_lock)
    def get_url(cls, url: str) -> BaseURLData:
        """
        Returns URL data if it is in the storage. Otherwise,
        returns None.
        """
        return cls._storage.get_url_data(url)

    @classmethod
    @thread_lock(_lock)
    def has_url(cls, url: str) -> bool:
        """Returns if any URL data has the same URL path as given."""
        return cls._storage.has_url(url)

    @classmethod
    @thread_lock(_lock)
    def add_discarded_url(cls, url: str, reason: str):
        """Sets URL is discarded."""
        cls.pop_url(url)
        return cls.add_url(DiscardedURL(url, reason))

    @classmethod
    @thread_lock(_lock)
    def increase_downloaded_amount(cls, url: str, new_content_size: int):
        """Increases a downloaded content amount for the given URL data."""
        url_data = cls.get_url(url)
        if not (url_data and isinstance(url_data, InProcessURLData)):
            return False
        return cls.update_url_data(url_data.url, downloaded=url_data.downloaded + new_content_size)
