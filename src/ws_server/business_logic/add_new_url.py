from exceptions.server_exceptions import WrongRequestData
from http_client.models.storages.url_pipe import URLPipe


class AddNewURL:
    """Adds a new URL to be downloaded by background workers."""

    async def execute(self, url_to_download: str):
        """Executes the command."""
        if url_to_download is None:
            raise WrongRequestData("You haven't specified a URL that must be downloaded.")
        elif not isinstance(url_to_download, str):
            raise WrongRequestData("The URL must be a string.")
        return await self.url_pipe.push(url_to_download)

    def __init__(self):
        """Saves a URL pipe which is listened by workers."""
        self.url_pipe = URLPipe()
