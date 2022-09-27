import pytest

from http_client.data_storage.storages.url_storage import URLStorage, URLType


@pytest.mark.http_client
class TestURLStorage:

    @pytest.fixture
    def url_storage(self):
        yield URLStorage()
        URLStorage.reset_storage()

    def test_exception_raised_with_wrong_storage_key(self, url_storage):
        with pytest.raises(KeyError):
            url_storage['2']

    def test_url_storage_properties_is_lists(self, url_storage):
        url_types = [URLType.TO_DOWNLOAD, URLType.DISCARDED, URLType.FINISHED]
        for url_type in url_types:
            random_value = 'some value'
            url_storage.add(random_value, url_type)
        assert isinstance(url_storage.urls_to_download, list)
        assert isinstance(url_storage.discarded, list)
        assert isinstance(url_storage.finished, list)
        assert len(url_storage.discarded) == 1
        assert len(url_storage.urls_to_download) == 1
        assert len(url_storage.finished) == 1

    def test_adding_to_different_url_type_storages(self, url_storage):
        url_storage.add('hi world', URLType.TO_DOWNLOAD)
        assert url_storage.urls_to_download != url_storage.finished
        assert url_storage.urls_to_download != url_storage.discarded
        assert 'hi world' in url_storage.urls_to_download

        url_storage.add('discarded url', URLType.DISCARDED)
        assert url_storage.urls_to_download != url_storage.finished
        assert url_storage.urls_to_download != url_storage.discarded
        assert len(url_storage.urls_to_download) == 1
        assert len(url_storage.discarded) == 1
        assert 'discarded url' in url_storage.discarded

    def test_pop_url_to_download(self, url_storage):
        assert url_storage.pop_url_to_download() is None
        url_storage.add('hi world1', URLType.TO_DOWNLOAD)
        url_storage.add('hi world2', URLType.TO_DOWNLOAD)
        url_storage.add('hi world3', URLType.TO_DOWNLOAD)
        assert url_storage.pop_url_to_download() == 'hi world1'
        assert url_storage.pop_url_to_download() == 'hi world2'
        assert url_storage.pop_url_to_download() == 'hi world3'
        assert url_storage.pop_url_to_download() is None

    def test_storage_reset(self, url_storage):
        url_storage.add('hi world1', URLType.TO_DOWNLOAD)
        url_storage.add('hi world2', URLType.TO_DOWNLOAD)
        url_storage.add('hi world3', URLType.TO_DOWNLOAD)
        assert url_storage.urls_to_download
        url_storage.reset_storage()
        assert not url_storage.urls_to_download
