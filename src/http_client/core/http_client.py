import asyncio

from http_client.core.workers_manager import WorkersManager
from http_client.models.storages.url_pipe import URLPipe


class HTTPClient:
    """
    Starts an HTTP-client for downloading a URL content
    in background.
    """

    def start(self):
        """
        Spawns background workers and starts listening a URL pipe
        for new URL.
        """
        self.workers_manager.start_workers()
        asyncio.create_task(self.listen_for_new_url())

    async def listen_for_new_url(self):
        """
        Listens for new added URLs and delegates them to the
        workers' handler.
        """
        while True:
            added_url = await URLPipe.pop()
            asyncio.create_task(self.workers_manager.dispatch_url(added_url))

    def __init__(self, workers_manager: WorkersManager):
        self.workers_manager = workers_manager
