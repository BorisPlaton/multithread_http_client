from http_client.utils.singleton import Singleton
from http_client.models.storages.url_workers import URLWorkersStorage


class URLWorkersRepository(metaclass=Singleton):
    """The repository to access a DAO with URL workers statuses."""

    _storage = URLWorkersStorage

    def get_workers_amount(self, url):
        """Returns a workers amount."""
        return self._storage.get_workers_amount(url)

    def increase_workers(self, url):
        """Increases a workers amount."""
        return self._storage.increase_workers(url)

    def decrease_workers(self, url):
        """Decreases a workers amount."""
        return self._storage.decrease_workers(url)

    def is_url_in_process(self, url):
        """Returns is a URL processing."""
        return self._storage.is_url_in_process(url)

    def restore(self):
        """Restore self storage."""
        self._storage.delete_all()
