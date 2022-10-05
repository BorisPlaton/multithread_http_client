from dataclasses import dataclass
from enum import Enum

from http_client.models.repositories.url_workers_repository import URLWorkersRepository


class ProcessStatus(Enum):
    """Defines the statuses of URL download work."""
    DISCARDED = 'Discarded'
    IN_PROCESS = 'In process'
    DOWNLOADED = 'Downloaded'


@dataclass(frozen=True)
class BaseURLData:
    """The base information about URL work. Is hashable."""
    url: str


@dataclass(frozen=True)
class DiscardedURL(BaseURLData):
    """The model of discarded URL."""
    reason: str
    process_status: ProcessStatus = ProcessStatus.DISCARDED


@dataclass(frozen=True)
class DownloadedURLData(BaseURLData):
    """The information about already downloaded data."""
    path_to_file: str
    process_status: ProcessStatus = ProcessStatus.DOWNLOADED


@dataclass(frozen=True)
class InProcessURLData(BaseURLData):
    """The information about a download work that is still in process."""
    total_length: int
    downloaded: int
    process_status: ProcessStatus = ProcessStatus.IN_PROCESS

    @property
    def progress(self) -> float:
        """Returns the progress of content downloading."""
        return round(self.downloaded / self.total_length, 4) * 100

    @property
    def workers_amount(self) -> int:
        """Returns workers quantity that are processing current URL."""
        return URLWorkersRepository.get_workers_amount(self.url)
