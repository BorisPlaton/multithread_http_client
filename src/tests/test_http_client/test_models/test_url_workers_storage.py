import pytest

from http_client.models.storages.url_workers import URLWorkersStorage


@pytest.mark.http_client
class TestURLWorkersStorage:

    @pytest.fixture
    def storage(self):
        yield URLWorkersStorage
        URLWorkersStorage.delete_all()

    def test_new_record_added_with_increasing_records_amount(self, storage):
        assert not storage._url_in_process.get('url')
        storage.increase_workers('url')
        assert storage._url_in_process.get('url') == 1

    def test_workers_amount_may_be_increased(self, storage):
        storage.increase_workers('url')
        storage.increase_workers('url')
        storage.increase_workers('url')
        assert storage._url_in_process.get('url') == 3

    def test_workers_amount_may_bet_decreased(self, storage):
        storage.increase_workers('url')
        storage.increase_workers('url')
        storage.decrease_workers('url')
        assert storage._url_in_process.get('url') == 1

    def test_workers_amount_record_is_deleted_if_it_equals_zero_or_less(self, storage):
        storage.increase_workers('url')
        assert storage._url_in_process.get('url') == 1
        storage.decrease_workers('url')
        assert storage._url_in_process.get('url') is None
        storage._url_in_process['url'] = -20
        storage.decrease_workers('url')
        assert storage._url_in_process.get('url') is None

    def test_get_workers_amount_is_correct(self, storage):
        storage.increase_workers('url')
        assert storage.get_workers_amount('url') == 1

    def test_workers_amount_is_zero_if_url_is_not_added(self, storage):
        assert storage.get_workers_amount('url') == 0

    def test_is_url_in_process(self, storage):
        storage.increase_workers('url')
        assert storage.is_url_in_process('url')
        assert not storage.is_url_in_process('url1')

    def test_storage_cleaning(self, storage):
        storage.increase_workers('url')
        storage.increase_workers('url1')
        storage.increase_workers('url2')
        assert len(storage._url_in_process) == 3
        storage.delete_all()
        assert len(storage._url_in_process) == 0

    def test_error_not_raised_if_decrease_not_existed_url(self, storage):
        assert storage._url_in_process.get('url') is None
        assert storage.decrease_workers('url') is None
