import pytest

from http_client.models.storages.structs import (
    BaseURLData, InProcessURLData,
    DownloadedURLData, DiscardedURL
)
from http_client.models.storages.url_statuses import URLStatusesStorage


@pytest.mark.http_client
class TestURLStatusesStorage:

    @pytest.fixture
    def storage(self):
        yield URLStatusesStorage
        URLStatusesStorage.delete_all()

    @pytest.fixture
    def discarded_url(self):
        return DiscardedURL('/', 'fail')

    @pytest.mark.parametrize(
        'wrong_url', [
            1, 2, 'str', str, BaseURLData, BaseURLData('2')
        ]
    )
    def test_wrong_url_data_type_cant_be_added(self, storage, wrong_url):
        with pytest.raises(ValueError):
            storage.add_url(wrong_url)

    @pytest.mark.parametrize(
        'correct_url', [
            DiscardedURL('s', 'fail'),
            DownloadedURLData('s', '/'),
            InProcessURLData('s', 1),
        ]
    )
    def test_only_base_url_data_type_can_be_added(self, storage, correct_url):
        assert not storage.add_url(correct_url)
        assert correct_url in storage.urls

    def test_pop_not_existed_url_not_cause_exception(self, storage):
        assert not storage.pop_url('url')

    @pytest.mark.parametrize(
        'wrong_type', [
            1, dict, DiscardedURL('/', 'fail'), str
        ]
    )
    def test_pop_url_with_wrong_type_raise_exception(self, storage, discarded_url, wrong_type):
        with pytest.raises(ValueError):
            storage.pop_url(wrong_type)

    def test_pop_url_returns_value(self, storage, discarded_url):
        storage.add_url(discarded_url)
        assert len(storage.urls) == 1
        pop_value = storage.pop_url(discarded_url.url)
        assert pop_value is discarded_url
        assert len(storage.urls) == 0

    def test_get_url_data_returns_correct_value(self, storage, discarded_url):
        storage.add_url(discarded_url)
        assert len(storage.urls) == 1
        assert storage.get_url_data(discarded_url.url) is discarded_url
        assert len(storage.urls) == 1

    def test_get_url_data_returns_none_if_not_valid_url_passed(self, storage, discarded_url):
        storage.add_url(discarded_url)
        assert storage.get_url_data('url') is None

    def test_has_url_returns_true_if_url_is_in_storage(self, storage, discarded_url):
        storage.add_url(discarded_url)
        assert storage.has_url(discarded_url.url) is True

    def test_has_url_returns_false_if_url_is_in_storage(self, storage, discarded_url):
        storage.add_url(discarded_url)
        assert storage.has_url('url') is False

    def test_delete_all_records_will_clean_storage(self, storage, discarded_url):
        storage.add_url(discarded_url)
        assert len(storage.urls) == 1
        storage.delete_all()
        assert len(storage.urls) == 0

    def test_storage_has_only_unique_values(self, storage, discarded_url):
        storage.add_url(discarded_url)
        storage.add_url(discarded_url)
        storage.add_url(discarded_url)
        assert len(storage.urls) == 1
