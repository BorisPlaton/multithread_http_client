from http_client.models.storages.structs import DownloadedContent


class ContentObserver:
    """
    Accepts the downloaded content of URL if it is fulled
    downloaded saves it and change its status in the storage.
    """

    def accept_content(self, url: str, downloaded_content: DownloadedContent):
        pass
