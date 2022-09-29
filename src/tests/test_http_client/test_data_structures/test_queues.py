import pytest

from http_client.data_structures.queues.base import BaseQueue


@pytest.mark.http_client
class TestBaseQueue:

    @pytest.fixture
    def queue(self):
        return BaseQueue()

    def test_push_new_element_to_queue(self, queue):
        queue.push('hello world')
        assert len(queue.queue) == 1

    def test_is_queue_empty(self, queue):
        assert not queue.is_filled
        queue.push('hello world')
        assert queue.is_filled

    def test_pop_element_from_queue(self, queue):
        queue.push('hello world')
        assert len(queue.queue) == 1
        assert queue.pop() == 'hello world'
        assert len(queue.queue) == 0
        assert queue.pop() is None
