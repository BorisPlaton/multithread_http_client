from dataclasses import dataclass
from enum import Enum


class ProcessStatus(Enum):
    """Defines the statuses of URL download work."""
    DISCARDED = 'Discarded'
    IN_PROCESS = 'In process'
    FINISHED = 'Finished'


@dataclass
class BaseURLData:
    """The base information about URL work."""
    url: str
    process_status: ProcessStatus


@dataclass
class DiscardedURL(BaseURLData):
    """The model of discarded URL."""
    reason: str


@dataclass
class DownloadedURLData(BaseURLData):
    """The information about already downloaded data."""
    path_to_file: str


@dataclass
class ProcessedURLData(BaseURLData):
    """The information about a downloading work that is still in process."""
    total_length: int
    downloaded: int

    @property
    def progress(self) -> float:
        """Returns the progress of content downloading."""
        return round(self.downloaded / self.total_length, 2) * 100

    @property
    def workers_amount(self) -> int:
        """Returns workers quantity that are processing current URL."""
        pass
