import asyncio
import time
from pathlib import Path

import pytest

from settings import settings
from http_client.core.http_client import HTTPClient
from http_client.utils.builders.builders import HTTPClientBuilder


@pytest.mark.system_test
class TestHTTPClientSystem:

    @pytest.fixture
    def http_client(self) -> HTTPClient:
        settings.THREADS_AMOUNT = 5
        settings.BYTES_AMOUNT = 10000
        return HTTPClientBuilder.construct()

    @pytest.mark.asyncio
    async def test_content_is_downloaded(self, http_client, content_dir, url_statuses_repository):
        settings.CONTENT_DIRECTORY = content_dir
        url = 'https://www.gravatar.com/avatar/a549deb942a43c8ea746f15dc629dde4?s=64&d=identicon&r=PG&f=1'

        http_client.workers_manager.start_workers()
        await http_client.add_url_to_dispatcher(url)
        time.sleep(3)
        http_client.workers_manager.stop_workers()

        url_data = url_statuses_repository.get_url(url)
        assert url_statuses_repository.is_downloaded(url_data)
        assert Path(url_data.path_to_file).exists()

    @pytest.mark.asyncio
    async def test_content_is_not_downloaded_if_wrong_url(self, http_client, content_dir, url_statuses_repository):
        settings.CONTENT_DIRECTORY = content_dir
        url = 'it is wrong url'

        await http_client.add_url_to_dispatcher(url)
        await asyncio.sleep(0.01)

        url_data = url_statuses_repository.get_url(url)
        assert url_statuses_repository.is_discarded(url_data)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'url',
        [
            'https://developer.mozilla.org',
            'https://docs.pytest.org/en/7.1.x/_static/documentation_options.js'

        ]
    )
    async def test_content_is_not_downloaded_if_wrong_response_data(
            self, http_client, content_dir, url_statuses_repository, url
    ):
        settings.CONTENT_DIRECTORY = content_dir

        await http_client.add_url_to_dispatcher(url)
        await asyncio.sleep(0.5)

        url_data = url_statuses_repository.get_url(url)
        assert url_statuses_repository.is_discarded(url_data)
