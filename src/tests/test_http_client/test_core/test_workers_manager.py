from unittest.mock import patch, MagicMock

import pytest

from exceptions.client_exceptions import URLDataException, ValidationException
from http_client.core.task_scheduler import Task
from http_client.core.workers_manager import WorkersManager
from http_client.utils.builders.builders import WorkersManagerBuilder
from http_client.utils.web_clients.url_info import URLResourceData


@pytest.mark.http_client
class TestWorkersManager:

    @pytest.fixture
    def workers_manager(self) -> WorkersManager:
        manager = WorkersManagerBuilder.construct()
        return manager

    def test_if_url_is_discarded_or_downloaded_exception_raised(self, workers_manager, url_statuses_repository):
        downloaded_url = '/'
        url_statuses_repository.add_url_to_downloaded(downloaded_url, 'path')
        with pytest.raises(URLDataException):
            workers_manager.check_task_url(downloaded_url)
        discarded_url = '/new/one'
        url_statuses_repository.add_url_to_discarded(discarded_url, 'reason')
        with pytest.raises(URLDataException):
            workers_manager.check_task_url(discarded_url)

    def test_if_url_is_in_process_exception_is_not_risen(self, workers_manager, url_statuses_repository):
        in_process_url = '/'
        url_statuses_repository.add_url_to_in_process(in_process_url, 500)
        assert not workers_manager.check_task_url(in_process_url)

    def test_url_is_added_to_in_process_if_new_tasks_for_workers_are_pushed(self, workers_manager,
                                                                            url_statuses_repository):
        url_content_data = URLResourceData('/', 500)
        workers_manager.create_new_tasks_for_workers(url_content_data)
        url_data_in_process = url_statuses_repository.get_url(url_content_data.url)
        assert url_statuses_repository.is_in_process(url_data_in_process)
        assert url_data_in_process.summary_size == url_content_data.summary_size

    def test_task_queue_contains_new_tasks_when_tasks_are_created(self, workers_manager, url_statuses_repository):
        url_content_data = URLResourceData('/', 500)
        assert not workers_manager.task_queue
        workers_manager.create_new_tasks_for_workers(url_content_data)
        assert workers_manager.task_queue
        for task in workers_manager.task_queue:
            assert isinstance(task, Task)

    @pytest.mark.asyncio
    @patch("http_client.core.workers_manager.URLInfoReceiver.get_url_data_if_valid")
    async def test_if_url_data_validation_exception_was_risen_url_added_to_discarded(
            self, get_url_mock: MagicMock, workers_manager, url_statuses_repository
    ):
        reason = 'some reason'

        async def risen_validation_exception(*args, **kwargs):
            raise ValidationException(reason)

        get_url_mock.side_effect = risen_validation_exception
        dispatched_url = '/'
        await workers_manager.dispatch_url(dispatched_url)
        url_data = url_statuses_repository.get_url(dispatched_url)
        assert url_statuses_repository.is_discarded(url_data)
        assert url_data.reason == reason

    @pytest.mark.asyncio
    @patch("http_client.core.workers_manager.WorkersManager.check_task_url")
    async def test_if_url_data_exception_was_risen_nothing_happen(
            self, check_url_mock: MagicMock, workers_manager, url_statuses_repository
    ):
        def rise_data_exception(*args, **kwargs):
            raise URLDataException

        check_url_mock.side_effect = rise_data_exception
        assert not await workers_manager.dispatch_url('/')
