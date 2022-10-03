from exceptions.client_exceptions import ValidationException
from http_client.background_workers.workers_handler import WorkersHandler
from http_client.builders.abstract_builder import AbstractBuilder
from http_client.core.client_controller import HTTPClient
from http_client.task_handling.task_scheduler import TaskScheduler
from http_client.url_consuming.url_listener import URLPipeListener
from http_client.web_clients.url_info import URLInfoReceiver


class TaskSchedulerBuilder(AbstractBuilder):
    """Builds a Task Scheduler."""

    instance_class = TaskScheduler
    bytes_amount: int

    @staticmethod
    def validate_bytes_amount(value, value_type: type):
        """Validates `bytes_amount` is greater than 0."""
        if value <= 0:
            raise ValidationException("The bytes amount can't be less than zero.")


class WorkersHandlerBuilder(AbstractBuilder):
    """Builds a Workers Handler."""

    instance_class = WorkersHandler
    workers_amount: int

    @staticmethod
    def validate_workers_amount(value, value_type: type):
        """Validates a `workers_amount` is greater than 0."""
        if value <= 0:
            raise ValidationException("Workers amount can't be less then 0.")


class HTTPClientBuilder(AbstractBuilder):
    """Builds an HTTP-client."""

    instance_class = HTTPClient
    task_scheduler: TaskScheduler
    url_pipe_listener: URLPipeListener
    url_info_receiver: URLInfoReceiver
    workers_handler: WorkersHandler
