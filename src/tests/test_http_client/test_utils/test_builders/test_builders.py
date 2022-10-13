import pytest

from http_client.core.content_observer import ContentObserver
from http_client.core.http_client import HTTPClient
from http_client.core.task_scheduler import TaskScheduler
from http_client.core.workers import TaskWorker
from http_client.core.workers_manager import WorkersManager
from http_client.models.storages.task_queue import TaskQueue
from http_client.utils.builders.builders import HTTPClientBuilder, WorkersManagerBuilder, TaskSchedulerBuilder, \
    TaskWorkerBuilder, ContentObserverBuilder, FileSaverBuilder
from http_client.utils.file_saver import FileSaver


@pytest.mark.http_client
class TestBuilders:

    def test_http_client_is_built(self):
        assert isinstance(HTTPClientBuilder.construct(), HTTPClient)

    def test_workers_manager_is_built(self):
        assert isinstance(WorkersManagerBuilder.construct(), WorkersManager)

    def test_workers_manager_and_workers_has_common_task_queue(self):
        workers_manager: WorkersManager = WorkersManagerBuilder.construct()
        for worker in workers_manager.workers:
            assert workers_manager.task_queue is worker.task_queue

    def test_task_scheduler_is_built(self):
        assert isinstance(TaskSchedulerBuilder.construct(), TaskScheduler)

    def test_task_worker_is_built(self):
        worker_builder = TaskWorkerBuilder()
        worker_builder.task_queue = TaskQueue()
        worker_builder.content_observer = ContentObserverBuilder.construct()
        assert isinstance(worker_builder.build(), TaskWorker)

    def test_file_saver_is_built(self):
        assert isinstance(FileSaverBuilder.construct(), FileSaver)

    def test_content_observer_is_built(self):
        assert isinstance(ContentObserverBuilder.construct(), ContentObserver)
