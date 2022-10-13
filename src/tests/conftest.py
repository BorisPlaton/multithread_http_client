import shutil
from pathlib import Path

import pytest

from http_client.models.repositories.url_statuses_repository import URLStatusesRepository


@pytest.fixture
def url_statuses_repository():
    storage = URLStatusesRepository()
    yield storage
    storage.restore()


@pytest.fixture
def content_dir():
    directory = Path(__file__).parent.parent.parent / 'downloaded_content'
    yield directory
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass
