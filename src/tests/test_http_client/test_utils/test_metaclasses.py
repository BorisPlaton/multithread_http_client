import time
from threading import Thread

import pytest

from http_client.utils.metaclasses import Singleton, ThreadSafe, ThreadSafeSingleton


@pytest.mark.http_client
class TestSingleton:

    def test_all_instances_are_the_same(self):
        class A(metaclass=Singleton):
            pass

        instances_list = []

        for _ in range(100):
            instances_list.append(A())

        assert len(set(map(id, instances_list))) == 1


@pytest.mark.http_client
class TestThreadSafe:

    def test_instance_method_is_locked_when_called(self):
        class A(metaclass=ThreadSafe):

            def method1(self):
                time.sleep(0.05)

        a = A()
        assert a._lock
        assert getattr(a.__class__, '_lock', None) is None
        a.method1()
        Thread(target=a.method1).start()
        assert not a._lock.acquire(blocking=False)

    def test_instances_have_different_lock(self):
        class A(metaclass=ThreadSafe):

            def method1(self):
                time.sleep(0.05)

        a = A()
        b = A()
        Thread(target=a.method1).start()
        assert not a._lock.acquire(blocking=False)
        assert b._lock.acquire(blocking=False)


@pytest.mark.http_client
class TestThreadSafeSingleton:

    def test_instances_method_are_locked_when_called(self):
        class A(metaclass=ThreadSafeSingleton):

            def method1(self):
                time.sleep(0.01)

        a = A()
        Thread(target=a.method1).start()
        assert not a._lock.acquire(blocking=False)

    def test_instances_locks_are_the_same(self):
        class A(metaclass=ThreadSafeSingleton):

            def method1(self):
                time.sleep(0.01)

        a = A()
        b = A()
        c = A()
        assert b._lock is a._lock
        assert b._lock is c._lock
        Thread(target=a.method1).start()
        assert not a._lock.acquire(blocking=False)
        assert not b._lock.acquire(blocking=False)
        assert not c._lock.acquire(blocking=False)

    def test_all_instances_are_the_same(self):
        class A(metaclass=ThreadSafeSingleton):

            def method1(self):
                time.sleep(0.01)

        instances_list = []

        def create_instance():
            nonlocal instances_list
            instances_list.append(A())

        threads = [Thread(target=create_instance) for _ in range(100)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(set(map(id, instances_list))) == 1
