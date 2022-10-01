from asyncio import Queue


class URLPipe:
    """The async pipe for adding new urls to download."""

    async def push(self, url_to_download: str):
        """Adds a new url to the pipe."""
        await self.queue.put(url_to_download)

    async def pop(self) -> str:
        """Pops an added url or waits until a new one will be added."""
        return await self.queue.get()

    def __init__(self):
        self.queue = Queue()
