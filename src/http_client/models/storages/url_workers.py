class URLWorkers:
    """Shows how many workers are processing specific URLs."""

    _url_in_process: dict[str, int] = {}

    @classmethod
    def increase_url_workers(cls, url):
        """Increases the workers quantity of URL."""
        if not cls.is_url_in_process(url):
            cls._url_in_process[url] = 0
        cls._url_in_process[url] += 1

    @classmethod
    def decrease_url_workers(cls, url):
        """
        Decreases the quantity of URL workers. If after decrease
        workers amount is 0, deletes it from observing.
        """
        if not cls.is_url_in_process(url):
            return
        cls._url_in_process[url] -= 1
        if cls._url_in_process[url] <= 0:
            cls._url_in_process.pop(url)

    @classmethod
    def get_url_workers_amount(cls, url) -> int:
        """
        Returns workers amount that are processing a URL.
        If URL isn't in a process, returns 0.
        """
        return cls._url_in_process.get(url, 0)

    @classmethod
    def is_url_in_process(cls, url):
        """Returns if a URL is processing."""
        return url in cls._url_in_process
