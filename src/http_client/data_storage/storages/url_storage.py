from enum import Enum, auto
from typing import TypeAlias

from http_client.data_storage.data_collections.implemented_collections import SetCollection, QueueCollection


AvailableURLStorages: TypeAlias = QueueCollection | SetCollection


class URLType(Enum):
    """Defines types of urls in an url storage."""
    TO_DOWNLOAD = auto()
    FINISHED = auto()
    DISCARDED = auto()


class URLStorage:
    """Stores urls data and provides an interface to communicate with it."""

    _url_type_storages = {
        URLType.TO_DOWNLOAD: QueueCollection(),
        URLType.FINISHED: SetCollection(),
        URLType.DISCARDED: SetCollection(),
    }

    def add(self, url: str, url_type: URLType):
        """Adds an url to a corresponding url type storage."""
        return self[url_type].add(url)

    def remove(self, url: str, url_type: URLType):
        """Removes an url from a corresponding url type storage."""
        return self[url_type].remove(url)

    def pop_url_to_download(self):
        """
        Pops the first url from an url storage which contains urls which
        must be downloaded.
        """
        return self[URLType.TO_DOWNLOAD].pop()

    @property
    def urls_to_download(self):
        """Returns a list of urls which must be downloaded."""
        return list(self[URLType.TO_DOWNLOAD])

    @property
    def finished(self):
        """Returns a list of urls which are already downloaded."""
        return list(self[URLType.FINISHED])

    @property
    def discarded(self):
        """
        Returns a list of urls which were not downloaded due to different
        reasons.
        """
        return list(self[URLType.DISCARDED])

    @classmethod
    def reset_storage(cls):
        """Sets new data collections for urls."""
        for url_type, data_storage in cls._url_type_storages.items():
            cls._url_type_storages[url_type] = data_storage.__class__()

    def __getitem__(self, urls_type: URLType) -> AvailableURLStorages:
        """Returns a corresponding urls storage."""
        try:
            return self._url_type_storages[urls_type]
        except KeyError:
            raise KeyError(
                f"The URLs storage which type is `{urls_type}` doesn't exist."
            )
