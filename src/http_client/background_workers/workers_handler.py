from collections import deque
from threading import Thread

from exceptions.client_exceptions import URLCantBeProcessed
from http_client.background_workers.workers import TaskWorker
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.models.storages.task_queue import TaskQueue
from http_client.task_handling.structs import Task


class WorkersHandler:
    """Handles workers creation and communication with them."""

    def spawn_workers(self):
        """Spawns and starts task workers in separate threads."""
        for _ in range(self.workers_amount):
            self.start_worker(self.create_worker())

    def add_task_for_workers(self, task: Task):
        """
        Adds a new task in task queue which is listened by
        workers.
        """
        try:
            self.check_task_url(task.url)
            self.task_queue.push(task)
        except URLCantBeProcessed:
            pass

    def check_task_url(self, task_url: str):
        """
        Check that URL isn't already downloaded or isn't
        discarded.
        """
        if task_url in self._forbidden_urls:
            raise URLCantBeProcessed
        elif URLStatusesRepository.is_discarded(task_url) or URLStatusesRepository.is_downloaded(task_url):
            self._forbidden_urls.appendleft(task_url)
            raise URLCantBeProcessed

    @staticmethod
    def start_worker(worker: TaskWorker):
        """Starts a worker in a new thread."""
        worker_thread = Thread(target=worker.start)
        worker_thread.start()

    def create_worker(self) -> TaskWorker:
        """Creates the new instance of worker with its task queue."""
        return TaskWorker(self.task_queue)

    def __init__(self, workers_amount: int, task_queue: TaskQueue):
        """Saves a workers amount and a task queue for them."""
        self.workers_amount = workers_amount
        self.task_queue = task_queue
        self._forbidden_urls = deque(maxlen=5)
