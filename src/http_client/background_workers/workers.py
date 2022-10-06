from exceptions.client_exceptions import ContentWasNotDownloaded
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
        """
        Starts worker to listen a task queue. When a new task
        is got starts processing it.
        """
        while True:
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

    def decode_downloaded_content(self, content: bytes) -> bytes:
        pass

    def download_url_content(self, task: Task) -> bytes:
        """Performs the downloading operation of URL content."""
        content = self.url_content_downloader.get_url_content(
            task.url, task.byte_range_start, task.byte_range_end
        )
        return content

    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue
        self.url_content_downloader = URLContentDownloader()
