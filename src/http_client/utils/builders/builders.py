from pathlib import Path

from exceptions.client_exceptions import ValidationException
from http_client.core.content_observer import ContentObserver
from http_client.core.workers import TaskWorker
from http_client.core.workers_manager import WorkersManager
from http_client.utils.builders.abstract_builder import AbstractBuilder
from http_client.core.http_client import HTTPClient
from http_client.models.storages.task_queue import TaskQueue
from http_client.core.task_scheduler import TaskScheduler
from http_client.utils.file_saver import FileSaver
from settings import settings


class HTTPClientBuilder(AbstractBuilder):
    """Builds an HTTP-client."""

    instance_class = HTTPClient
    workers_manager: WorkersManager

    def configure_instance(self):
        """Saves the instance of Workers Manager."""
        self.workers_manager = WorkersManagerBuilder.construct()


class WorkersManagerBuilder(AbstractBuilder):
    """Builds a Workers Manager."""

    instance_class = WorkersManager
    task_queue: TaskQueue
    task_scheduler: TaskScheduler
    workers: list[TaskWorker]

    def configure_instance(self):
        """Creates a task scheduler, task queue and workers."""
        self.task_scheduler = TaskSchedulerBuilder.construct()
        self.task_queue = TaskQueue()

        content_observer = ContentObserverBuilder.construct()
        self.workers = []
        for _ in range(settings.THREADS_AMOUNT):
            worker_builder = TaskWorkerBuilder()
            worker_builder.task_queue = self.task_queue
            worker_builder.content_observer = content_observer
            self.workers.append(worker_builder.build())

    @staticmethod
    def validate_workers_list(value):
        """Validates a workers list."""
        if not value:
            raise ValidationException("The workers list can't be empty.")
        elif not all((map(lambda x: isinstance(x, TaskWorker), value))):
            raise ValidationException("Values in workers list must be a `TaskWorker` type.")
        if len(value) != settings.settings.THREADS_AMOUNT:
            raise ValidationException(
                f"Workers amount must be {settings.settings.THREADS_AMOUNT}. But it is {len(value)}."
            )


class TaskSchedulerBuilder(AbstractBuilder):
    """Builds a Task Scheduler."""

    instance_class = TaskScheduler
    bytes_amount: int

    def configure_instance(self):
        """Sets bytes amount from the settings."""
        self.bytes_amount = settings.BYTES_AMOUNT

    @staticmethod
    def validate_bytes_amount(value):
        """Validates `bytes_amount` is greater than 0."""
        if value <= 0:
            raise ValidationException("The bytes amount can't be less than zero.")


class TaskWorkerBuilder(AbstractBuilder):
    """Builds a TaskWorker instance."""

    instance_class = TaskWorker
    task_queue: TaskQueue
    content_observer: ContentObserver

    def configure_instance(self):
        """Sets bytes amount from the settings."""
        self.task_queue = TaskQueue()
        self.content_observer = ContentObserverBuilder.construct()


class FileSaverBuilder(AbstractBuilder):
    """Builds a FileSaver instance."""

    instance_class = FileSaver
    files_directory: Path

    def configure_instance(self):
        """Sets a directory which will contain all downloaded content."""
        self.files_directory = settings.CONTENT_DIRECTORY


class ContentObserverBuilder(AbstractBuilder):
    """Builds a ContentObserve instance."""

    instance_class = ContentObserver
    file_saver: FileSaver

    def configure_instance(self):
        """Sets a directory which will contain all downloaded content."""
        self.file_saver = FileSaverBuilder.construct()
