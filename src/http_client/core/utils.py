from functools import wraps
from threading import Lock


def thread_lock(lock: Lock):
    """Wraps called function with Lock to make it thread-safe."""

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return inner

    return wrapper


def instance_thread_lock(lock_name: str):
    """
    Wraps called an instance method with instance's Lock.
    Gets it via `lock_name` parameter which shows an
    instance's field with Lock instance.
    """

    def wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            instance_lock = getattr(self, lock_name)
            with instance_lock:
                return func(self, *args, **kwargs)

        return inner

    return wrapper
