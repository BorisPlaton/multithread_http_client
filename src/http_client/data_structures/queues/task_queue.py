from http_client.data_structures.queues.base import BaseQueue
from http_client.task_handling.structs import Task


class TaskQueue(BaseQueue):
    """It is a base queue but only changes typing in methods on `Task`."""

    def push(self, new_task: Task):
        return self.queue.append(Task)

    def pop(self) -> Task:
        return self.queue.popleft()
