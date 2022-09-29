from http_client.data_structures.queues.task_queue import TaskQueue


class TaskScheduler:
    """Creates new tasks for workers and adds them to a task queue."""

    async def get_url_data(self, url_to_validate):
        pass

    async def create_new_task_for_url(self, url: str):
        url_data = await self.get_url_data(url)

    def __init__(self, task_queue: TaskQueue):
        """Saves a task queue to put new tasks in the future."""
        self.task_queue = task_queue
