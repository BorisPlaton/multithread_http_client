from exceptions.base import ApplicationException
from exceptions.client_exceptions import URLDataException
from http_client.core.workers import TaskWorker
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.models.storages.task_queue import TaskQueue
from http_client.core.task_scheduler import TaskScheduler
from http_client.utils.web_clients.url_info import URLInfoReceiver, URLResourceData


class WorkersManager:
    """
    Defines interface to communicate with workers via
    a task pipe. May set up data about tasks for workers.
    """

    def start_workers(self):
        """Starts all workers in separate threads."""
        for worker in self.workers:
            worker.start()

    def stop_workers(self):
        """Stops all workers that are observed."""
        for worker in self.workers:
            worker.stop()

    async def dispatch_url(self, task_url: str):
        """
        Checks if URL isn't already processed, validates data about its
        content and creates new tasks for workers.
        """
        try:
            self.check_task_url(task_url)
            url_content_data = await URLInfoReceiver.get_url_data_if_valid(task_url)
            self.create_new_tasks_for_workers(url_content_data)
        except ApplicationException as e:
            self.url_statuses.add_url_to_discarded(task_url, e.detail)
        except Exception as e:
            self.url_statuses.add_url_to_discarded(task_url, repr(e))

    def create_new_tasks_for_workers(self, url_content_data: URLResourceData):
        """
        Marks the URL of content as in process and generates tasks for
        workers.
        """
        self.url_statuses.add_url_to_in_process(url_content_data.url, url_content_data.summary_size)
        for task in self.task_scheduler.generate_new_tasks(url_content_data.url, url_content_data.summary_size):
            self.task_queue.push(task)

    def check_task_url(self, task_url: str):
        """
        Check that URL isn't already downloaded or isn't
        discarded.
        """
        if self.url_statuses.is_discarded(task_url) or self.url_statuses.is_downloaded(task_url):
            raise URLDataException

    def __init__(self, task_scheduler: TaskScheduler, task_queue: TaskQueue, workers: list[TaskWorker]):
        """Saves a task scheduler, background workers and their task queue."""
        self.task_scheduler = task_scheduler
        self.task_queue = task_queue
        self.workers = workers
        self.url_statuses = URLStatusesRepository()
