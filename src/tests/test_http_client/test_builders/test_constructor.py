import pytest

from http_client.background_workers.workers_handler import WorkersHandler
from http_client.builders.constructor import ComponentsConstructor
from http_client.core.client_controller import HTTPClient
from http_client.task_handling.task_scheduler import TaskScheduler


class TestComponentsConstructor:

    @pytest.fixture
    def constructor(self):
        return ComponentsConstructor

    def test_task_scheduler_is_constructed(self):
        assert isinstance(ComponentsConstructor.construct_task_scheduler(), TaskScheduler)

    def test_workers_handler_is_constructed(self):
        assert isinstance(ComponentsConstructor.construct_workers_handler(), WorkersHandler)

    def test_http_client_is_constructed(self):
        assert isinstance(ComponentsConstructor.construct_http_client(), HTTPClient)
