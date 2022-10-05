import asyncio

from exceptions.client_exceptions import ValidationException
from http_client.background_workers.workers_handler import WorkersHandler
from http_client.models.repositories.url_statuses_repository import URLStatusesRepository
from http_client.task_handling.task_scheduler import TaskScheduler
from http_client.url_consuming.url_listener import URLPipeListener
from http_client.web_clients.url_info import URLInfoReceiver


class HTTPClient:

    async def listen_for_new_url(self):
        while True:
            added_url = await self.url_pipe_listener.get_url_from_pipe()
            self.start_processing_url_if_new(added_url)

    def start_processing_url_if_new(self, url_for_task: str):
        if not URLStatusesRepository.has_url(url_for_task):
            asyncio.create_task(self.delegate_new_task(url_for_task))

    async def delegate_new_task(self, url_for_task: str):
        try:
            url_content_data = await self.url_info_receiver.get_url_data_if_valid(url_for_task)
        except ValidationException as e:
            URLStatusesRepository.add_discarded_url(url_for_task, e.detail)

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
