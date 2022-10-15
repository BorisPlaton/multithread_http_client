from http_client.utils.metaclasses import ThreadSafeSingleton
from http_client.models.storages.structs import (
    DiscardedURL, InProcessURLData, DownloadedURLData, DownloadedContent
)
from http_client.models.storages.url_statuses import URLStatusesStorage, EXISTING_URL_TYPES


class URLStatusesRepository(metaclass=ThreadSafeSingleton):
    """
    The repository to interact with a URL storage. Has additional
    methods.
    """

    _storage = URLStatusesStorage

    def add_url(self, url_data: EXISTING_URL_TYPES):
        """
        Adds new URL data to the storage and pops old if it is
        existed.
        """
        self._storage.pop_url(url_data.url)
        return self._storage.add_url(url_data)

    def add_url_to_discarded(self, url: str, reason: str):
        """Sets URL is discarded."""
        return self.add_url(DiscardedURL(url, reason))

    def add_url_to_in_process(self, url: str, summary_size: int):
        """Adds a URL as in process to the storage."""
        return self.add_url(InProcessURLData(url, summary_size))

    def add_url_to_downloaded(self, url: str, path_to_file: str):
        """Adds a URL as in process to the storage."""
        return self.add_url(DownloadedURLData(url, path_to_file))

    def update_url_data(self, url: str, **kwargs) -> bool:
        """Adds new URL data to the storage."""
        if not (old_url_data := self._storage.pop_url(url)):
            return False
        url_data_fields = vars(old_url_data)
        url_data_fields.update({**kwargs})
        new_url_data = old_url_data.__class__(**url_data_fields)
        self.add_url(new_url_data)
        return True

    def pop_url(self, url: str):
        """
        Decreases the quantity of URL workers. If after decrease
        workers amount is 0, deletes it from observing.
        """
        return self._storage.pop_url(url)

    def get_url(self, url: str) -> EXISTING_URL_TYPES:
        """
        Returns URL data if it is in the storage. Otherwise,
        returns None.
        """
        return self._storage.get_url_data(url)

    def has_url(self, url: str) -> bool:
        """Returns if any URL data has the same URL path as given."""
        return self._storage.has_url(url)

    def check_status(self, url: str | EXISTING_URL_TYPES, url_status: type[EXISTING_URL_TYPES]):
        """Checks if URL data is a given status type."""
        if isinstance(url, str):
            url = self.get_url(url)
        return isinstance(url, url_status)

    def is_discarded(self, url_data: str | EXISTING_URL_TYPES) -> bool:
        """Returns if URL is discarded."""
        return self.check_status(url_data, DiscardedURL)

    def is_downloaded(self, url_data: str | EXISTING_URL_TYPES) -> bool:
        """Returns if URL is downloaded."""
        return self.check_status(url_data, DownloadedURLData)

    def is_in_process(self, url_data: str | EXISTING_URL_TYPES) -> bool:
        """Returns if URL is in process."""
        return self.check_status(url_data, InProcessURLData)

    def add_downloaded_content(self, url: str, downloaded_content: DownloadedContent):
        """Increases a downloaded content amount for the given URL data."""
        if self.is_in_process(url):
            self.get_url(url).add_downloaded_fragment(downloaded_content)

    def restore(self):
        """Deletes all records in the storage."""
        self._storage.delete_all()
