from typing import Callable


class Function:
    """
    The descriptor. When it `__get__` method is called,
    returns the instance of `SynchronizedMethod` class
    that if it is called, locks the instance lock.
    """

    def __init__(self, func: Callable, lock_attr: str):
        """
        Saves a class function and the attribute name of
        instance's lock.
        """
        self.func = func
        self.lock_attr = lock_attr

    def __get__(self, instance, owner):
        """Returns a thread-safe method."""
        return SynchronizedMethod(self.func, instance, getattr(instance, self.lock_attr))


class SynchronizedMethod:
    """
    Runs a saved function with a lock to make it
    thread-safe.
    """

    def __init__(self, func: Callable, instance, lock):
        """Saves a class function, its instance and instance's lock."""
        self.func = func
        self.instance = instance
        self.lock = lock

    def __call__(self, *args, **kwargs):
        """Makes a method and runs it with a lock."""
        with self.lock:
            return self.func(self.instance, *args, **kwargs)
