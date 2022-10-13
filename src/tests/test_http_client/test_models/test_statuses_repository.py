import pytest

from http_client.models.storages.structs import DiscardedURL, DownloadedURLData, InProcessURLData, ProcessStatus, \
    DownloadedContent


@pytest.mark.http_client
class TestURLStatusesRepository:

    @pytest.fixture
    def storage(self, url_statuses_repository):
        return url_statuses_repository._storage

    @pytest.fixture
    def discarded_url(self):
        return DiscardedURL('/', 'reason')

    @pytest.fixture
    def downloaded_url(self):
        return DownloadedURLData('/', 'file path')

    @pytest.fixture
    def in_process_url(self):
        return InProcessURLData('/', 500)

    @pytest.fixture
    def downloaded_content(self):
        return DownloadedContent(b'', 0)

    def test_is_downloaded_returns_false_if_not_downloaded(self, url_statuses_repository, discarded_url):
        url_statuses_repository.add_url(discarded_url)
        assert not url_statuses_repository.is_downloaded(discarded_url.url)

    def test_is_downloaded_returns_false_if_url_is_not_existed(self, url_statuses_repository):
        assert not url_statuses_repository.is_downloaded('/')

    def test_is_downloaded_returns_true_if_downloaded(self, url_statuses_repository, downloaded_url):
        url_statuses_repository.add_url(downloaded_url)
        assert url_statuses_repository.is_downloaded(downloaded_url.url)

    def test_is_discarded_returns_false_if_not_discarded(self, url_statuses_repository, downloaded_url):
        url_statuses_repository.add_url(downloaded_url)
        assert not url_statuses_repository.is_discarded(downloaded_url.url)

    def test_is_discarded_returns_false_if_url_is_not_existed(self, url_statuses_repository):
        assert not url_statuses_repository.is_discarded('/')

    def test_is_discarded_returns_true_if_discarded(self, url_statuses_repository, discarded_url):
        url_statuses_repository.add_url(discarded_url)
        assert url_statuses_repository.is_discarded(discarded_url.url)

    def test_is_in_process_returns_false_if_not_in_process(self, url_statuses_repository, discarded_url):
        url_statuses_repository.add_url(discarded_url)
        assert not url_statuses_repository.is_in_process(discarded_url.url)

    def test_is_in_process_returns_false_if_url_is_not_existed(self, url_statuses_repository):
        assert not url_statuses_repository.is_in_process('/')

    def test_is_in_process_returns_true_if_is_in_process(self, url_statuses_repository, in_process_url):
        url_statuses_repository.add_url(in_process_url)
        assert url_statuses_repository.is_in_process(in_process_url.url)

    def test_add_url_pop_old_data(self, url_statuses_repository, in_process_url, storage):
        url_statuses_repository.add_url(in_process_url)
        assert len(storage.urls) == 1
        url_statuses_repository.add_url(DownloadedURLData(in_process_url.url, 'path to file'))
        assert len(storage.urls) == 1
        assert url_statuses_repository.is_downloaded(in_process_url.url)

    def test_add_url_to_discarded_pop_old_url_data(self, url_statuses_repository, storage, in_process_url):
        url_statuses_repository.add_url(in_process_url)
        assert len(storage.urls) == 1
        assert url_statuses_repository.is_in_process(in_process_url.url)
        url_statuses_repository.add_url_to_discarded(in_process_url.url, 'discarded')
        assert len(storage.urls) == 1

        added_url_data: DiscardedURL = url_statuses_repository.get_url(in_process_url.url)
        assert url_statuses_repository.is_discarded(in_process_url.url)
        assert added_url_data.reason == 'discarded'
        assert added_url_data.url == in_process_url.url
        assert added_url_data.process_status == ProcessStatus.DISCARDED

    def test_add_url_to_downloaded_pop_old_url_data(self, url_statuses_repository, storage, in_process_url):
        url_statuses_repository.add_url(in_process_url)
        assert len(storage.urls) == 1
        assert url_statuses_repository.is_in_process(in_process_url.url)
        url_statuses_repository.add_url_to_downloaded(in_process_url.url, 'path to file')
        assert len(storage.urls) == 1

        added_url_data: DownloadedURLData = url_statuses_repository.get_url(in_process_url.url)
        assert url_statuses_repository.is_downloaded(in_process_url.url)
        assert added_url_data.path_to_file == 'path to file'
        assert added_url_data.url == in_process_url.url
        assert added_url_data.process_status == ProcessStatus.DOWNLOADED

    def test_add_url_to_in_process_pop_old_url_data(self, url_statuses_repository, storage, discarded_url):
        url_statuses_repository.add_url(discarded_url)
        assert len(storage.urls) == 1
        assert url_statuses_repository.is_discarded(discarded_url.url)
        url_statuses_repository.add_url_to_in_process(discarded_url.url, 200)
        assert len(storage.urls) == 1

        added_url_data: InProcessURLData = url_statuses_repository.get_url(discarded_url.url)
        assert url_statuses_repository.is_in_process(discarded_url.url)
        assert added_url_data.summary_size == 200
        assert added_url_data.downloaded_fragments == []
        assert added_url_data.process_status == ProcessStatus.IN_PROCESS

    def test_add_downloaded_content_works_only_for_in_process_url(self, url_statuses_repository, discarded_url,
                                                                  downloaded_content):
        url_statuses_repository.add_url(discarded_url)
        url_statuses_repository.add_downloaded_content(discarded_url.url, downloaded_content)
        url_statuses_repository.is_discarded(discarded_url)

    def test_add_downloaded_content_adds_content_for_in_process_url(
            self, url_statuses_repository, in_process_url, downloaded_content
    ):
        url_statuses_repository.add_url(in_process_url)
        assert not in_process_url.downloaded_fragments
        url_statuses_repository.add_downloaded_content(in_process_url.url, downloaded_content)
        assert in_process_url.downloaded_fragments
        assert len(in_process_url.downloaded_fragments) == 1
        assert in_process_url.downloaded_fragments[0] == downloaded_content

    def test_update_url_data_returns_false_if_url_is_not_existed(self, url_statuses_repository):
        assert not url_statuses_repository.update_url_data('/')

    def test_update_url_data_returns_true_and_set_new_value(self, url_statuses_repository, downloaded_content):
        in_process_url = InProcessURLData('/', 500)
        in_process_url.add_downloaded_fragment(downloaded_content)
        url_statuses_repository.add_url(in_process_url)
        assert url_statuses_repository.update_url_data(in_process_url.url, summary_size=1000)
        updated_data: InProcessURLData = url_statuses_repository.get_url(in_process_url.url)
        assert url_statuses_repository.is_in_process(updated_data.url)
        assert updated_data.summary_size == 1000
        assert updated_data.downloaded_fragments
        assert len(updated_data.downloaded_fragments) == 1
