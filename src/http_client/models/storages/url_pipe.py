from asyncio import Queue

from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.utils.metaclasses import Singleton


class URLPipe(metaclass=Singleton):
    """The async pipe for adding new urls to download."""

    async def push(self, url_to_download: str) -> bool:
        """Adds a new url to the pipe if it doesn't already exist."""
        if self.url_statuses.has_url(url_to_download):
            return False
        self.url_statuses.add_url_to_pending(url_to_download)
        await self.queue.put(url_to_download)
        return True

    async def pop(self) -> str:
        """Pops an added url or waits until a new one will be added."""
        url_to_download = await self.queue.get()
        self.url_statuses.pop_url(url_to_download)
        return url_to_download

    def __init__(self):
        self.queue = Queue()
        self.url_statuses = URLStatusesRepository()
