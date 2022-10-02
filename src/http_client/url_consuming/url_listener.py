from http_client.url_consuming.url_pipe import URLPipe


class URLPipeListener:
    """Listens a URL-pipe and returns added URLs."""

    @staticmethod
    async def get_url_from_pipe() -> str:
        """Waits and pops an added URL from a URL-pipe."""
        return await URLPipe.pop()
