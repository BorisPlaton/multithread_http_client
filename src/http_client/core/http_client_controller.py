import asyncio

from exceptions.client_exceptions import ValidationException
from http_client.background_workers.workers_handler import WorkersHandler
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.task_handling.task_scheduler import TaskScheduler
from http_client.url_consuming.url_listener import URLPipeListener
from http_client.web_clients.structs import URLResourceData
from http_client.web_clients.url_info import URLInfoReceiver


class HTTPClient:

    async def listen_for_new_url(self):
        while True:
            added_url = await self.url_pipe_listener.get_url_from_pipe()
            asyncio.create_task(self.delegate_new_task(added_url))

    async def delegate_new_task(self, url_for_task: str):
        try:
            url_content_data = await self.url_info_receiver.get_url_data_if_valid(url_for_task)
            self.create_new_tasks_for_workers(url_content_data)
        except ValidationException as e:
            URLStatusesRepository.add_url_to_discarded(url_for_task, e.detail)

    def create_new_tasks_for_workers(self, url_content_data: URLResourceData):
        for new_task in self.task_scheduler.generate_new_tasks(url_content_data):
            self.workers_handler.add_task_for_workers(new_task)

    def __init__(
            self,
            task_scheduler: TaskScheduler,
            url_pipe_listener: URLPipeListener,
            url_info_receiver: URLInfoReceiver,
            workers_handler: WorkersHandler,
    ):
        self.task_scheduler = task_scheduler
        self.url_pipe_listener = url_pipe_listener
        self.url_info_receiver = url_info_receiver
        self.workers_handler = workers_handler
