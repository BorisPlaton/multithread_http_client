from dataclasses import dataclass
from threading import RLock

from exceptions.client_exceptions import URLDataException
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.models.storages.structs import DownloadedContent, DownloadedURLData, InProcessURLData
from http_client.utils.file_saver import FileSaver
from http_client.utils.wrappers import instance_thread_lock


@dataclass
class ContentSizeProgress:
    """
    Shows how much of content was downloaded and point
    when all content will be downloaded.
    """
    summary_size: int
    downloaded_size: int = 0

    @property
    def is_downloaded(self) -> bool:
        """
        Returns `True` if downloaded content size equals
        to summary size.
        """
        return self.summary_size == self.downloaded_size


class ContentObserver:
    """
    Accepts the downloaded content of URL if it is fulled
    downloaded saves it and change its status in the storage.
    """

    @instance_thread_lock('_lock')
    def accept_content(self, url: str, downloaded_content: DownloadedContent):
        """Receives new downloaded content and saves it."""
        self.update_url_progress(url, downloaded_content.size)
        self.url_storage.add_downloaded_content(url, downloaded_content)
        self.save_as_file_if_ready(url)

    def update_url_progress(self, url: str, size: int):
        """Updates URL content downloading progress for internal needs."""
        try:
            if url not in self.url_progress:
                self.url_progress[url] = ContentSizeProgress(self.get_url_content_summary_size(url))
            self.url_progress[url].downloaded_size += size
        except URLDataException:
            pass

    def save_as_file_if_ready(self, url: str):
        """Saves data to file system if it is fully downloaded."""
        url_content_progress = self.url_progress.get(url)
        if isinstance(url_content_progress, ContentSizeProgress) and url_content_progress.is_downloaded:
            self.save_as_file(url)

    def get_url_content_summary_size(self, url) -> int:
        url_data = self.url_storage.get_url(url)
        if not self.url_storage.is_in_process(url_data):
            raise URLDataException("URL is not in process. Thus, it doesn't have the size of content.")
        return url_data.summary_size

    def save_as_file(self, url: str):
        """
        Marks URL as downloaded in the storage and saves its content to the file system.
        """
        self.url_progress.pop(url)
        url_data: InProcessURLData = self.url_storage.pop_url(url)
        path_to_file = self.file_saver.save_content_to_file_system(url_data.downloaded_content)
        self.url_storage.add_url_to_downloaded(url, path_to_file)

    def __init__(self, file_saver: FileSaver):
        self.url_progress: dict[str, ContentSizeProgress] = {}
        self.url_storage = URLStatusesRepository()
        self.file_saver = file_saver
        self._lock = RLock()
