from threading import Thread, Event, RLock

from exceptions.client_exceptions import ContentWasNotDownloaded
from http_client.core.wrappers import instance_thread_lock
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.models.repositories.url_workers_repository import URLWorkersRepository
from http_client.models.storages.task_queue import TaskQueue
from http_client.task_handling.structs import Task
from http_client.web_clients.url_content import URLContentDownloader


class TaskWorker:
    """
    The worker that is running in a separate thread. Downloads
    content from given URL and saves it.
    """

    def start(self):
        """Starts a worker's activity."""
        self.is_working = True
        Thread(target=self.listen_queue).start()

    def stop(self):
        """Stops the worker."""
        self.is_working = False

    def listen_queue(self):
        """
        Starts worker to listen a task queue. When a new task
        is got starts processing it.
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
        URLWorkersRepository.increase_workers(task.url)
        try:
            content = self.download_url_content(task)
            URLStatusesRepository.increase_downloaded_amount(task.url, task.content_size)
        except ContentWasNotDownloaded as e:
            URLStatusesRepository.add_url_to_discarded(task.url, e.detail)
        finally:
            URLWorkersRepository.decrease_workers(task.url)

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
        if not isinstance(value, bool):
            raise ValueError(
                "To set if the worker is working you must pass a boolean argument."
            )
        self._is_working.set() if value else self._is_working.clear()

    def __init__(self, task_queue: TaskQueue):
        """Saves a task queue which will be listened to."""
        self.task_queue = task_queue
        self._is_working = Event()
        self._lock = RLock()
