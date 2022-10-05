from threading import Lock

from http_client.core.utils import thread_lock
from http_client.models.storages.srtucts import (
    BaseURLData, ProcessStatus, DiscardedURL,
    DownloadedURLData, InProcessURLData
)
from http_client.models.storages.url_statuses import URLStatusesStorage


class URLStatusesRepository:
    """
    The repository to interact with a URL storage. Has additional
    methods.
    """

    _storage = URLStatusesStorage
    _lock = Lock()

    @classmethod
    @thread_lock(_lock)
    def add_url(cls, url):
        """Increases the workers quantity of URL."""
        return cls._storage.add_url(url)

    @classmethod
    @thread_lock(_lock)
    def pop_url(cls, url: BaseURLData | str):
        """
        Decreases the quantity of URL workers. If after decrease
        workers amount is 0, deletes it from observing.
        """
        return cls._storage.pop_url(url)

    @classmethod
    @thread_lock(_lock)
    def get_url_data(cls, url: str) -> BaseURLData:
        """
        Returns URL data if it is in the storage. Otherwise,
        returns None.
        """
        return cls._storage.get_url_data(url)

    @classmethod
    @thread_lock(_lock)
    def has_url(cls, url: str):
        """Returns if any URL data has the same URL path as given."""
        return cls._storage.has_url(url)

    @classmethod
    @thread_lock(_lock)
    def update_status(cls, url: BaseURLData | str, change_to: ProcessStatus, **kwargs):
        """
        Changes the status of URL data to a new one. If the URL
        doesn't exist, does nothing.
        """
        if not (old_url_data := cls._storage.pop_url(url)):
            return
        new_url_data = cls.change_url_type(old_url_data, change_to, **kwargs)
        cls._storage.add_url(new_url_data)
        return new_url_data

    @classmethod
    @thread_lock(_lock)
    def change_url_type(cls, url_data: BaseURLData, new_process_status: ProcessStatus, **kwargs):
        """
        Creates the new instance of URL data with the same URL but
        another process status and other fields.
        """
        if new_process_status == ProcessStatus.DISCARDED:
            url_type = DiscardedURL
        elif new_process_status == ProcessStatus.IN_PROCESS:
            url_type = DownloadedURLData
        elif new_process_status == ProcessStatus.DOWNLOADED:
            url_type = InProcessURLData
        else:
            raise ValueError(f"Not existed URL type - {new_process_status}")
        return url_type(url=url_data.url, process_status=new_process_status, **kwargs)
