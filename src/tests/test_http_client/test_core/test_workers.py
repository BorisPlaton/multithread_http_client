import threading
from unittest.mock import patch, MagicMock

import pytest

from exceptions.client_exceptions import ContentWasNotDownloaded
from http_client.core.task_scheduler import Task
from http_client.core.workers import TaskWorker
from http_client.utils.builders.builders import TaskWorkerBuilder


@pytest.mark.http_client
class TestTaskWorker:

    @pytest.fixture
    def worker(self) -> TaskWorker:
        return TaskWorkerBuilder.construct()

    def test_worker_starts_work_in_separate_thread(self, worker):
        try:
            worker.start()
            assert len(threading.enumerate()) == 2
            assert worker.is_working
        finally:
            worker.stop()

    def test_threads_stops_when_worker_stops(self, worker):
        try:
            worker.start()
            assert len(threading.enumerate()) == 2
            worker_thread = worker._thread
            worker.stop()
            worker_thread.join()
            assert len(threading.enumerate()) == 1
        finally:
            worker.stop()

    @patch('http_client.core.workers.TaskWorker.download_url_content')
    def test_url_added_to_discarded_if_content_was_not_downloaded(
            self, downloaded_content_mock: MagicMock, worker, url_statuses_repository
    ):
        reason = 'some reason'

        def raise_not_downloaded(*args, **kwargs):
            raise ContentWasNotDownloaded(reason)

        url = '/'

        downloaded_content_mock.side_effect = raise_not_downloaded
        worker.process_task(Task(url, 0, 100))

        url_data = url_statuses_repository.get_url(url)
        assert url_statuses_repository.is_discarded(url_data)
        assert url_data.reason == reason
