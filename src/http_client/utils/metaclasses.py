import inspect
from threading import Lock, RLock

from http_client.utils.descriptors import Function
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
            cls.__instances[cls] = cls.__create_new_instance(*args, **kwargs)
        return cls.__instances[cls]

    @thread_lock(__lock)
    def __create_new_instance(cls, *args, **kwargs):
        """
        Creates a default instance in the thread-safe way.
        """
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class ThreadSafe(type):
    """
    The metaclass makes all instance methods thread-safe
    by wrapping them in a Lock.
    """

    __lock_attr = '_lock'

    def __call__(cls, *args, **kwargs):
        """
        Creates a new instance and wraps all its methods
        with Lock.
        """
        instance = super().__call__(*args, **kwargs)
        setattr(instance, cls.__lock_attr, RLock())
        return instance

    def __new__(mcs, *args, **kwargs):
        new_class = super().__new__(mcs, *args, **kwargs)
        mcs.__make_methods_thread_safe(new_class)
        return new_class

    @classmethod
    def __make_methods_thread_safe(mcs, class_instance):
        """
        Wraps all methods via RLock to make them thread-safe.
        """
        for attr, value in vars(class_instance).items():
            if inspect.isfunction(value) and not (attr.startswith('__') and attr.endswith('__')):
                setattr(
                    class_instance, attr, Function(value, mcs.__lock_attr)
                )


class ThreadSafeSingleton(Singleton, ThreadSafe):
    """
    Makes instances a singleton and makes their methods
    thread-safe.
    """
