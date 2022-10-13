import time
from threading import Thread

import pytest

from http_client.utils.singleton import Singleton


@pytest.mark.http_client
class TestSingleton:

    @pytest.fixture
    def singleton(self):
        return Singleton

    def test_all_instances_are_the_same(self):
        class A(metaclass=Singleton):
            pass

        instances_list = []

        for _ in range(100):
            instances_list.append(A())

        assert len(set(map(id, instances_list))) == 1

    def test_instances_method_are_locked_when_called(self):
        class A(metaclass=Singleton):

            def method1(self):
                time.sleep(0.01)

        a = A()
        Thread(target=a.method1).start()
        assert not a._lock.acquire(blocking=False)
