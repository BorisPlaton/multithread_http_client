from http_client.models.storages.task_queue import TaskQueue
from http_client.url_consuming.url_listener import URLPipeListener
from http_client.web_clients.url_info import URLInfoReceiver
from settings import settings
from http_client.builders.builders import TaskSchedulerBuilder, WorkersHandlerBuilder, HTTPClientBuilder


class ComponentsConstructor:
    """Creates the components of HTTP-client package."""

    @classmethod
    def construct_task_scheduler(cls):
        """Creates a Task Scheduler instance."""
        builder = TaskSchedulerBuilder()
        builder.bytes_amount = settings.BYTES_AMOUNT
        return builder.build()

    @classmethod
    def construct_workers_handler(cls):
        """Creates a Workers Handler instance."""
        builder = WorkersHandlerBuilder()
        builder.workers_amount = settings.THREADS_AMOUNT
        builder.task_queue = TaskQueue()
        return builder.build()

    @classmethod
    def construct_http_client(cls):
        """Creates an HTTP-client instance."""
        task_scheduler = cls.construct_task_scheduler()
        workers_handler = cls.construct_workers_handler()
        builder = HTTPClientBuilder()
        builder.task_scheduler = task_scheduler
        builder.workers_handler = workers_handler
        builder.url_info_receiver = URLInfoReceiver()
        builder.url_pipe_listener = URLPipeListener()
        return builder.build()
