from http_client.models.repositories.url_statuses_repository import URLStatusesRepository


class GetAllURLStatuses:

    def execute(self) -> list[dict]:
        """Returns all statuses from the URL storage."""
        return [url_status.info for url_status in self.url_statuses.get_all_url()]

    def __init__(self):
        self.url_statuses = URLStatusesRepository()
