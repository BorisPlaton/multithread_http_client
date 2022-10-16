from http_client.models.repositories.url_statuses_repository import URLStatusesRepository


class GetAllURLStatuses:
    """Returns all statuses from the URL storage."""

    def execute(self) -> list[dict]:
        """Executes the command."""
        return [url_status.info for url_status in self.url_statuses.get_all_url()]

    def __init__(self):
        """Saves a repository with all URL statuses."""
        self.url_statuses = URLStatusesRepository()
