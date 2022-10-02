from exceptions.base import ApplicationException
from http_client.background_workers.workers_handler import WorkersHandler
from http_client.builders.abstract_builder import AbstractBuilder
from http_client.task_handling.task_scheduler import TaskScheduler


class TaskSchedulerBuilder(AbstractBuilder):
    """Builds a Task Scheduler."""

    instance_class = TaskScheduler
    bytes_amount: int

    @staticmethod
    def validate_bytes_amount(value):
        """Validates `bytes_amount` is greater than 0."""
        if value <= 0:
            raise ApplicationException("The bytes amount can't be less than zero.")


class WorkersHandlerBuilder(AbstractBuilder):
    """Builds a Workers Handler."""

    instance_class = WorkersHandler
    workers_amount: int

    @staticmethod
    def validate_workers_amount(value):
        """Validates a `workers_amount` is greater than 0."""
        if value < 1:
            raise ApplicationException("Workers amount can't be less then 0.")
