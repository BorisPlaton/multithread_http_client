import inspect
from threading import Lock, RLock

from http_client.utils.wrappers import thread_lock


class Singleton(type):
    """
    The metaclass for implementing the Singleton
    pattern. It is thread-safe and wraps all class methods
    by RLock.
    """

    __instances = {}
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Creates a new instance if it doesn't exist. To make
        the Singleton thread-safe uses a Double-checked locking
        pattern.
        """
        if cls not in cls.__instances:
            cls.__instances[cls] = cls.__create_new_instance(cls, *args, **kwargs)
        return cls.__instances[cls]

    @thread_lock(__lock)
    def __create_new_instance(cls, instance_class: type, *args, **kwargs):
        """
        Creates a default instance and wraps its methods
        with RLock.
        """
        if instance_class not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
            cls.__make_methods_thread_safe(cls)
        return cls.__instances[cls]

    @staticmethod
    def __make_methods_thread_safe(instance_class):
        """
        Wraps all methods via RLock to make them thread-safe.
        """
        instance_lock = RLock()
        instance_class._lock = instance_lock
        for attr, value in vars(instance_class).items():
            if inspect.isfunction(value):
                setattr(
                    instance_class, attr, thread_lock(instance_lock)(value)
                )
