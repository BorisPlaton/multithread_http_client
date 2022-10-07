import pytest

from http_client.background_workers.workers_spawner import WorkersSpawner
from http_client.builders.constructor import ComponentsConstructor
from http_client.core.http_client import HTTPClient
from http_client.task_handling.task_scheduler import TaskScheduler


class TestComponentsConstructor:

    @pytest.fixture
    def constructor(self):
        return ComponentsConstructor

    def test_task_scheduler_is_constructed(self):
        assert isinstance(ComponentsConstructor.construct_task_scheduler(), TaskScheduler)

    def test_workers_handler_is_constructed(self):
        assert isinstance(ComponentsConstructor.construct_workers_handler(), WorkersSpawner)

    def test_http_client_is_constructed(self):
        assert isinstance(ComponentsConstructor.construct_http_client(), HTTPClient)
