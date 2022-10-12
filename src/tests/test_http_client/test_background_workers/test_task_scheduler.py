import pytest

from http_client.core.task_scheduler import TaskScheduler, Task
from http_client.utils.web_clients.url_info import URLResourceData


@pytest.mark.http_client
class TestTaskScheduler:

    @pytest.fixture
    def scheduler(self):
        return TaskScheduler(400)

    @pytest.fixture
    def url_resource_data(self):
        return URLResourceData('/', 1000)

    @pytest.mark.parametrize(
        'bytes_amount, content_length, byte_ranges',
        [
            (500, 2000, [(0, 499), (500, 999), (1000, 1499), (1500, 1999)]),
            (500, 2001, [(0, 499), (500, 999), (1000, 1499), (1500, 1999), (2000, 2000)]),
            (600, 500, [(0, 499)]),
            (500, 500, [(0, 499)]),
            (499, 500, [(0, 498), (499, 499)]),
        ])
    def test_get_byte_ranges_return_correct_ranges(self, scheduler, bytes_amount, content_length, byte_ranges):
        scheduler.bytes_amount = bytes_amount
        total_content_length = content_length
        assert list(scheduler.generate_byte_ranges(total_content_length)) == byte_ranges

    def test_task_generation(self, scheduler, url_resource_data):
        generated_tasks = list(scheduler.generate_new_tasks(url_resource_data.url, url_resource_data.summary_length))
        assert list(generated_tasks)
        for task in generated_tasks:
            assert isinstance(task, Task)
