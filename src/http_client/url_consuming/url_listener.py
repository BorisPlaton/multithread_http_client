from http_client.url_consuming.url_pipe import URLPipe


class URLPipeListener:
    """Listens a URL-pipe and returns added URLs."""

    async def listen_pipe(self) -> str:
        """
        Listens a URL-pipe. If a new URL is received returns it.
        """
        while True:
            return await self.get_url_from_pipe()

    async def get_url_from_pipe(self) -> str:
        """Waits and pops an added URL from a URL-pipe."""
        return await self.url_pipe.pop()

    def __init__(self, url_pipe: URLPipe):
        """
        Saves an url pipe which will be listened.
        """
        self.url_pipe = url_pipe
