from dataclasses import dataclass
from enum import Enum

from http_client.models.repositories.url_workers_repository import URLWorkersRepository


class ProcessStatus(Enum):
    """Defines the statuses of URL download work."""
    DISCARDED = 'Discarded'
    IN_PROCESS = 'In process'
    DOWNLOADED = 'Downloaded'


@dataclass
class BaseURLData:
    """The base information about URL work."""
    url: str
    process_status: ProcessStatus


@dataclass
class DiscardedURL(BaseURLData):
    """The model of discarded URL."""
    process_status = ProcessStatus.DISCARDED
    reason: str


@dataclass
class DownloadedURLData(BaseURLData):
    """The information about already downloaded data."""
    process_status = ProcessStatus.DOWNLOADED
    path_to_file: str


@dataclass
class InProcessURLData(BaseURLData):
    """The information about a download work that is still in process."""
    process_status = ProcessStatus.IN_PROCESS
    total_length: int
    downloaded: int

    @property
    def progress(self) -> float:
        """Returns the progress of content downloading."""
        return round(self.downloaded / self.total_length, 4) * 100

    @property
    def workers_amount(self) -> int:
        """Returns workers quantity that are processing current URL."""
        return URLWorkersRepository.get_workers_amount(self.url)
