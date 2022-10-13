from threading import Thread, Event, RLock

from exceptions.client_exceptions import ContentWasNotDownloaded
from http_client.core.content_observer import ContentObserver
from http_client.core.task_scheduler import Task
from http_client.utils.web_clients.url_content import URLContentDownloader
from http_client.utils.wrappers import instance_thread_lock
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.models.repositories.url_workers_repository import URLWorkersRepository
from http_client.models.storages.structs import DownloadedContent
from http_client.models.storages.task_queue import TaskQueue


class TaskWorker:
    """
    The worker that is running in a separate thread. Downloads
    content from given URL and saves it.
    """

    @instance_thread_lock('_lock')
    def start(self):
        """Starts a worker's activity."""
        if not self._thread.is_alive():
            self.is_working = True
            self._thread.start()

    @instance_thread_lock('_lock')
    def stop(self):
        """Stops the worker."""
        if self._thread.is_alive():
            self.is_working = False
            self._thread = self._get_thread_instance()

    def listen_queue(self):
        """
        Starts the worker to listen a task queue. When
        a new task is got, starts to process it.
        """
        while self.is_working:
            new_task = self.task_queue.pop()
            if new_task:
                self.process_task(new_task)

    def process_task(self, task: Task):
        """
        Starts process task. Changes the workers amount of task's URL.
        Download content. If it fails to download, adds to discarded.
        """
        self._url_workers_repository.increase_workers(task.url)
        try:
            content = self.download_url_content(task)
            self.content_observer.accept_content(
                task.url, DownloadedContent(content, task.byte_range_start)
            )
        except ContentWasNotDownloaded as e:
            self._url_repository.add_url_to_discarded(task.url, e.detail)
        finally:
            self._url_workers_repository.decrease_workers(task.url)

    @staticmethod
    def download_url_content(task: Task) -> bytes:
        """Performs the downloading operation of URL content."""
        content = URLContentDownloader.get_url_content(
            task.url, task.byte_range_start, task.byte_range_end
        )
        return content

    @property
    @instance_thread_lock('_lock')
    def is_working(self):
        """Returns if the worker is working."""
        return self._is_working.is_set() or False

    @is_working.setter
    @instance_thread_lock('_lock')
    def is_working(self, value: bool):
        """
        Sets if the worker is executing his job. A value must be a
        boolean type.
        """
        if not isinstance(value, bool):
            raise ValueError(
                "To set if the worker is working you must pass a boolean argument."
            )
        self._is_working.set() if value else self._is_working.clear()

    def _get_thread_instance(self) -> Thread:
        return Thread(target=self.listen_queue)

    def __init__(self, task_queue: TaskQueue, content_observer: ContentObserver):
        """Saves a task queue which will be listened to."""
        self.task_queue = task_queue
        self.content_observer = content_observer
        self._thread = self._get_thread_instance()
        self._is_working = Event()
        self._lock = RLock()
        self._url_repository = URLStatusesRepository()
        self._url_workers_repository = URLWorkersRepository()
