from exceptions.client_exceptions import URLCantBeProcessed, ValidationException
from http_client.background_workers.workers import TaskWorker
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.models.storages.task_queue import TaskQueue
from http_client.task_handling.task_scheduler import TaskScheduler
from http_client.web_clients.structs import URLResourceData
from http_client.web_clients.url_info import URLInfoReceiver


class WorkersManager:
    """
    Defines interface to communicate with workers via
    a task pipe. May set up data about tasks for workers.
    """

    def start_workers(self):
        """Starts all workers in separate threads."""
        for worker in self.workers:
            worker.start()

    async def dispatch_url(self, task_url: str):
        """
        Checks if URL isn't already processed, validates data about its
        content and creates new tasks for workers.
        """
        try:
            self.check_task_url(task_url)
            url_content_data = await URLInfoReceiver.get_url_data_if_valid(task_url)
            self.create_new_tasks_for_workers(url_content_data)
        except ValidationException as e:
            URLStatusesRepository.add_url_to_discarded(task_url, e.detail)
        except URLCantBeProcessed:
            pass

    def create_new_tasks_for_workers(self, url_content_data: URLResourceData):
        """
        Marks the URL of content as in process and generates tasks for
        workers.
        """
        URLStatusesRepository.add_url_to_in_process(url_content_data.url, url_content_data.summary_length)
        for task in self.task_scheduler.generate_new_tasks(url_content_data):
            self.task_queue.push(task)

    @staticmethod
    def check_task_url(task_url: str):
        """
        Check that URL isn't already downloaded or isn't
        discarded.
        """
        if URLStatusesRepository.is_discarded(task_url) or URLStatusesRepository.is_downloaded(task_url):
            raise URLCantBeProcessed

    def __init__(self, task_scheduler: TaskScheduler, task_queue: TaskQueue, workers: list[TaskWorker]):
        """Saves a task scheduler, background workers and their task queue."""
        self.task_scheduler = task_scheduler
        self.task_queue = task_queue
        self.workers = workers
