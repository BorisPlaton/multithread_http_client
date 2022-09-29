import asyncio

from http_client.data_structures.pipes.url_pipe import URLPipe
from http_client.task_handling.scheduler import TaskScheduler


class URLPipeConsumer:
    """
    Receives new urls from an url pipe and invokes a task scheduler
    to create new tasks.
    """

    async def listen_pipe(self):
        """
        Listens an url pipe. If a new url is received invokes a task scheduler.
        """
        while True:
            new_url = await self.url_pipe.pop()
            self.invoke_task_scheduler(new_url)

    def invoke_task_scheduler(self, new_url: str):
        """Invokes a scheduler to create a new tasks for workers."""
        asyncio.create_task(self.task_scheduler.create_new_task_for_url(new_url))

    def __init__(self, task_scheduler: TaskScheduler, url_pipe: URLPipe):
        """
        Saves a task scheduler which will be invoked if a new url is received from
        an url pipe.
        """
        self.task_scheduler = task_scheduler
        self.url_pipe = url_pipe
