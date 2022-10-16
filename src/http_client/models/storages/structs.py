from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property

from http_client.models.repositories.url_workers_repository import URLWorkersRepository


class ProcessStatus(Enum):
    """Defines the statuses of URL download work."""
    PENDING = 'In Pending'
    DISCARDED = 'Discarded'
    IN_PROCESS = 'In Process'
    DOWNLOADED = 'Downloaded'

    def __repr__(self):
        return self.value


@dataclass
class DownloadedContent:
    """Defines the part of the downloaded content of URL."""
    content: bytes
    byte_range_start: int

    @cached_property
    def size(self):
        """
        Returns the size of `content`. After first evaluating
        will be cached.
        """
        return len(self.content)


@dataclass(frozen=True)
class BaseURLData:
    """The base information about URL work. Is hashable."""
    url: str

    @property
    def info(self) -> dict:
        """Returns base information about URL."""
        base_data = {}
        base_data.update(vars(self))
        return base_data


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
class PendingURL(BaseURLData):
    """Indicates that URL is still pending."""
    process_status: ProcessStatus = ProcessStatus.PENDING


@dataclass(frozen=True)
class InProcessURLData(BaseURLData):
    """The information about a download work that is still in process."""
    summary_size: int
    downloaded_fragments: list[DownloadedContent] = field(default_factory=list, compare=False, hash=False)
    process_status: ProcessStatus = ProcessStatus.IN_PROCESS

    @property
    def info(self):
        base_data = super().info
        base_data.pop('downloaded_fragments')
        base_data.update({
            'progress': self.progress,
            'downloaded_content_size': self.downloaded_content_size,
            'workers_amount': self.workers_amount,
        })
        return base_data

    @property
    def downloaded_content_size(self) -> int:
        """Returns the total amount of all downloaded fragments."""
        return sum([fragment.size for fragment in self.downloaded_fragments])

    @property
    def downloaded_content(self) -> bytes:
        """Returns all downloaded content as bytes."""
        return b''.join([
            fragment.content for fragment in sorted(
                [fragment for fragment in self.downloaded_fragments],
                key=lambda x: x.byte_range_start
            )
        ])

    @property
    def progress(self) -> float:
        """Returns the progress of content downloading in percents."""
        return round(self.downloaded_content_size / self.summary_size, 4)

    @property
    def workers_amount(self) -> int:
        """Returns workers quantity that are processing current URL."""
        return URLWorkersRepository().get_workers_amount(self.url)

    def add_downloaded_fragment(self, downloaded_content: DownloadedContent):
        """Adds a downloaded content to already existed content fragments."""
        if not isinstance(downloaded_content, DownloadedContent):
            raise ValueError(
                "Only a `DownloadedContent` type can be used to add downloaded "
                "fragments, not a `{type(downloaded_content)}`."
            )
        self.downloaded_fragments.append(downloaded_content)
