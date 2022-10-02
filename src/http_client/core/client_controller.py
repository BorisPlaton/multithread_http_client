from http_client.background_workers.workers_handler import WorkersHandler
from http_client.task_handling.task_scheduler import TaskScheduler
from http_client.url_consuming.url_listener import URLPipeListener
from http_client.web_clients.url_info import URLInfoReceiver


class HTTPClient:

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
