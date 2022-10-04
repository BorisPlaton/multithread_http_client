from functools import wraps
from threading import Lock


def thread_lock(func):
    """Wraps called function with Lock to make it thread-safe."""

    @wraps(func)
    def inner(*args, **kwargs):
        with Lock():
            return func(*args, **kwargs)

    return inner
