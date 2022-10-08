from http_client.models.storages.structs import DownloadedURLData, DiscardedURL, InProcessURLData


EXISTING_URL_TYPES = InProcessURLData | DiscardedURL | DownloadedURLData


class URLStatusesStorage:
    """The storage of different URLs types."""

    urls: set[EXISTING_URL_TYPES] = set()

    @classmethod
    def add_url(cls, url: EXISTING_URL_TYPES):
        """Adds a new URL to storage."""
        if not isinstance(url, EXISTING_URL_TYPES):
            raise ValueError(f"URL data can't be a `{type(url)}` type.")
        cls.urls.add(url)

    @classmethod
    def pop_url(cls, url: str) -> EXISTING_URL_TYPES | None:
        """
        Removes and returns URL data from the storage. If it doesn't
        exist, returns None.
        """
        if not isinstance(url, str):
            raise ValueError(f"The URL to pop must be `str` not `{type(url)}` type.")
        return_value = None
        try:
            return_value = cls.get_url_data(url) if isinstance(url, str) else url
            cls.urls.remove(return_value)
        except KeyError:
            pass
        return return_value

    @classmethod
    def get_url_data(cls, url: str) -> EXISTING_URL_TYPES:
        """
        Returns URL data if it is in the storage. Otherwise,
        returns None.
        """
        try:
            return [url_data for url_data in cls.urls if url_data.url == url][0]
        except IndexError:
            pass

    @classmethod
    def has_url(cls, url: str) -> bool:
        """Returns if any URL data has the same URL path as given."""
        return url in [url_data.url for url_data in cls.urls]

    @classmethod
    def delete_all(cls):
        """Deletes all records in the storage."""
        cls.urls = set()
