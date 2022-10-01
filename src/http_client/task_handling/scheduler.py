from http_client.task_handling.structs import Task
from http_client.web_clients.structs import URLResourceData


class TaskScheduler:
    """Creates new tasks for workers."""

    def create_new_tasks(self, url_data: URLResourceData) -> list[Task]:
        pass

    def _get_bytes_ranges(self) -> list[tuple(int, int)]:
        pass
