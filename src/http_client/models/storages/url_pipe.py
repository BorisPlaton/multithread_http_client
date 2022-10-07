from asyncio import Queue


class URLPipe:
    """The async pipe for adding new urls to download."""

    queue = Queue()

    @classmethod
    async def push(cls, url_to_download: str):
        """Adds a new url to the pipe."""
        await cls.queue.put(url_to_download)

    @classmethod
    async def pop(cls) -> str:
        """Pops an added url or waits until a new one will be added."""
        return await cls.queue.get()
