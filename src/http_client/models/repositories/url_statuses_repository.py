from threading import RLock

from http_client.utils.wrappers import thread_lock
from http_client.models.storages.structs import (
    DiscardedURL, InProcessURLData, DownloadedURLData, DownloadedContent
)
from http_client.models.storages.url_statuses import URLStatusesStorage, EXISTING_URL_TYPES


class URLStatusesRepository:
    """
    The repository to interact with a URL storage. Has additional
    methods.
    """

    _storage = URLStatusesStorage
    _lock = RLock()

    @classmethod
    @thread_lock(_lock)
    def add_url(cls, url_data: EXISTING_URL_TYPES):
        """
        Adds new URL data to the storage and pops old if it is
        existed.
        """
        cls._storage.pop_url(url_data.url)
        return cls._storage.add_url(url_data)

    @classmethod
    @thread_lock(_lock)
    def add_url_to_discarded(cls, url: str, reason: str):
        """Sets URL is discarded."""
        return cls.add_url(DiscardedURL(url, reason))

    @classmethod
    @thread_lock(_lock)
    def add_url_to_in_process(cls, url: str, summary_size: int):
        """Adds a URL as in process to the storage."""
        return cls.add_url(InProcessURLData(url, summary_size))

    @classmethod
    @thread_lock(_lock)
    def add_url_to_downloaded(cls, url: str, path_to_file: str):
        """Adds a URL as in process to the storage."""
        return cls.add_url(DownloadedURLData(url, path_to_file))

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
    def get_url(cls, url: str) -> EXISTING_URL_TYPES:
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
    def is_discarded(cls, url: str) -> bool:
        """Returns if any URL data has the same URL path as given."""
        return isinstance(cls.get_url(url), DiscardedURL)

    @classmethod
    @thread_lock(_lock)
    def is_downloaded(cls, url: str) -> bool:
        """Returns if any URL data has the same URL path as given."""
        return isinstance(cls.get_url(url), DownloadedURLData)

    @classmethod
    @thread_lock(_lock)
    def is_in_process(cls, url: str) -> bool:
        """Returns if any URL data has the same URL path as given."""
        return isinstance(cls.get_url(url), InProcessURLData)

    @classmethod
    @thread_lock(_lock)
    def add_downloaded_content(cls, url: str, downloaded_content: DownloadedContent):
        """Increases a downloaded content amount for the given URL data."""
        if cls.is_in_process(url):
            cls.get_url(url).add_downloaded_fragment(downloaded_content)

    @classmethod
    @thread_lock(_lock)
    def restore(cls):
        """Deletes all records in the storage."""
        cls._storage.delete_all()
