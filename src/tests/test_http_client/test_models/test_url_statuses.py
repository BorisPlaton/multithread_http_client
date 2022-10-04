import pytest

from http_client.models.storages.srtucts import BaseURLData, ProcessStatus, InProcessURLData, DownloadedURLData, \
    DiscardedURL
from http_client.models.storages.url_statuses import URLStatusesStorage


@pytest.mark.http_client
class TestURLStatusesStorage:

    @pytest.fixture
    def storage(self):
        yield URLStatusesStorage
        URLStatusesStorage.delete_all()

    @pytest.mark.parametrize(
        'wrong_url', {
            1, 2, 'str', str, BaseURLData
        }
    )
    def test_wrong_url_data_type_cant_be_added(self, storage, wrong_url):
        with pytest.raises(ValueError):
            storage.add_url(wrong_url)

    @pytest.mark.parametrize(
        'correct_url', {
            BaseURLData('s', ProcessStatus.IN_PROCESS),
            DiscardedURL('s', ProcessStatus.IN_PROCESS, 'fail'),
            DownloadedURLData('s', ProcessStatus.IN_PROCESS, '/'),
            InProcessURLData('s', ProcessStatus.IN_PROCESS, 1, 2),
        }
    )
    def test_only_base_url_data_type_can_be_added(self, storage, correct_url):
        assert storage.add_url(correct_url)
        assert correct_url in storage.urls
