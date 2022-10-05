import time
from threading import Lock, Thread

import pytest

from http_client.core.utils import thread_lock, instance_thread_lock


@pytest.mark.http_client
class TestCoreUtils:

    def test_thread_lock_locks_funcs(self):
        lock = Lock()

        @thread_lock(lock)
        def some_func():
            time.sleep(0.1)

        Thread(target=some_func).start()
        assert lock.locked()

    def test_instance_thread_lock_locks_methods(self):
        class A:

            @instance_thread_lock('some_lock')
            def method(self):
                time.sleep(0.1)

            def __init__(self):
                self.some_lock = Lock()

        instance = A()
        assert not instance.some_lock.locked()
        Thread(target=instance.method).start()
        assert instance.some_lock.locked()
