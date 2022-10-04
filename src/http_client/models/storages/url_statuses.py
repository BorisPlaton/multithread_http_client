from http_client.models.storages.srtucts import BaseURLData


class URLStatusesStorage:
    """The storage of different URLs types."""

    urls: set[BaseURLData] = set()

    @classmethod
    def add_url(cls, url: BaseURLData):
        """Adds a new URL to storage."""
        if not isinstance(url, BaseURLData):
            raise ValueError("URL data must be a `BaseURLData` type.")
        cls.urls.add(url)

    @classmethod
    def pop_url(cls, url: BaseURLData | str) -> BaseURLData:
        """
        Removes and returns URL data from storage. If it doesn't
        exist, returns None.
        """
        return_value = None
        try:
            return_value = cls.get_url_data(url) if isinstance(url, str) else url
            cls.urls.remove(return_value)
        except KeyError:
            pass
        return return_value

    @classmethod
    def get_url_data(cls, url: str) -> BaseURLData:
        """
        Returns URL data if it is in the storage. Otherwise,
        returns None.
        """
        try:
            return [url_data for url_data in cls.urls if url_data.url == url][0]
        except IndexError:
            pass

    @classmethod
    def has_url(cls, url: str):
        """Returns if any URL data has the same URL path as given."""
        return url in [url_data.url for url_data in cls.urls]

    @classmethod
    def delete_all(cls):
        """Deletes all records in the storage."""
        cls.urls = set()
