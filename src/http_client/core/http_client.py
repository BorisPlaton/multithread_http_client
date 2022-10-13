import asyncio

from http_client.core.workers_manager import WorkersManager
from http_client.models.storages.url_pipe import URLPipe


class HTTPClient:
    """
    Starts an HTTP-client for downloading a URL content
    in background.
    """

    async def start(self):
        """
        Spawns background workers and starts listening a URL pipe
        for new URL.
        """
        self.workers_manager.start_workers()
        await self.listen_for_new_url()

    async def listen_for_new_url(self):
        """
        Listens for new added URLs and delegates them to the
        workers' handler.
        """
        while True:
            self.add_url_to_dispatcher(await URLPipe.pop())

    def add_url_to_dispatcher(self, url: str):
        """Creates a new task to execute it asynchronously."""
        return asyncio.create_task(self.workers_manager.dispatch_url(url))

    def __init__(self, workers_manager: WorkersManager):
        self.workers_manager = workers_manager
