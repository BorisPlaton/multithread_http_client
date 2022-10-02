from http_client.background_workers.workers_handler import WorkersHandler
from http_client.core.client_controller import HTTPClient
from http_client.task_handling.task_scheduler import TaskScheduler, TaskSchedulerBuilder
from http_client.url_consuming.url_listener import URLPipeListener
from http_client.web_clients.url_info import URLInfoReceiver
from settings import settings


class HTTPClientBuilder:
    """
    Build an HTTP-client. Creates necessary objects, and configures
    them.
    """

    def build(self):
        """Set up all components and returns an initialized HTTP-client with them."""
        return HTTPClient(
            self.task_scheduler,
            self.url_pipe_listener,
            self.url_info_receiver,
            self.workers_handler,
        )

    @staticmethod
    def get_task_scheduler():
        """Builds and returns an initialized Task Scheduler instance."""
        task_scheduler_builder = TaskSchedulerBuilder()
        task_scheduler_builder.bytes_amount = settings.BYTES_AMOUNT
        return task_scheduler_builder.build()

    @staticmethod
    def get_url_pipe_listener():
        return URLPipeListener()

    @staticmethod
    def get_url_info_receiver():
        return URLInfoReceiver()

    @staticmethod
    def get_workers_handler():
        return WorkersHandler(settings.THREADS_AMOUNT)

    def __init__(self):
        self.task_scheduler = self.get_task_scheduler()
        self.url_pipe_listener = self.get_url_pipe_listener()
        self.url_info_receiver = self.get_url_info_receiver()
        self.workers_handler = self.get_workers_handler()
