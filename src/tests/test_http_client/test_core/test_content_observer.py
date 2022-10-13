import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from exceptions.client_exceptions import URLDataException
from http_client.core.content_observer import ContentSizeProgress, ContentObserver
from http_client.utils.file_saver import FileSaver


@pytest.mark.http_client
class TestContentSizeProgressStruct:

    @pytest.mark.parametrize(
        'summary_size, is_downloaded',
        [
            [0, True],
            [1, False],
        ]

    )
    def test_is_downloaded_works_properly(self, summary_size, is_downloaded):
        content_size_progress = ContentSizeProgress(summary_size)
        assert content_size_progress.is_downloaded == is_downloaded


@pytest.mark.http_client
class TestContentObserver:

    @pytest.fixture
    def content_observer(self, file_saver):
        observer = ContentObserver(file_saver)
        yield observer
        observer.url_storage.restore()

    @pytest.fixture
    def file_saver(self, content_dir):
        return FileSaver(content_dir)

    @staticmethod
    def delete_dir(path_to_dir: Path):
        try:
            shutil.rmtree(path_to_dir)
        except FileNotFoundError:
            pass

    @patch('http_client.core.content_observer.ContentObserver.save_as_file')
    def test_file_will_not_be_saved_if_url_is_not_observed(self, save_method_mock: MagicMock, content_observer):
        was_called = False

        def save_as_file(*args, **kwargs):
            nonlocal was_called
            was_called = True

        save_method_mock.side_effect = save_as_file
        assert not content_observer.url_progress
        content_observer.save_as_file_if_ready('/')
        assert not was_called

    @patch('http_client.core.content_observer.ContentObserver.save_as_file')
    def test_file_will_not_be_saved_if_content_is_not_fully_downloaded(
            self, save_method_mock: MagicMock, content_observer
    ):
        was_called = False

        def save_as_file(*args, **kwargs):
            nonlocal was_called
            was_called = True

        save_method_mock.side_effect = save_as_file
        url = '/'
        content_observer.url_progress[url] = ContentSizeProgress(100)
        content_observer.save_as_file_if_ready(url)
        assert not was_called

    @patch('http_client.core.content_observer.ContentObserver.save_as_file')
    def test_file_is_saved_if_content_is_downloaded(self, save_method_mock: MagicMock, content_observer):
        was_called = False

        def save_as_file(*args, **kwargs):
            nonlocal was_called
            was_called = True

        save_method_mock.side_effect = save_as_file
        url = '/'
        content_observer.url_progress[url] = ContentSizeProgress(0)
        content_observer.save_as_file_if_ready(url)
        assert was_called

    def test_new_record_of_url_progress_will_be_created_if_it_doesnt_exist(self, content_observer,
                                                                           url_statuses_repository):
        assert not content_observer.url_progress
        url = '/'
        total_size = 1000
        downloaded_size = 10
        url_statuses_repository.add_url_to_in_process(url, total_size)
        content_observer.update_url_progress(url, downloaded_size)
        assert url in content_observer.url_progress
        url_progress = content_observer.url_progress[url]
        assert not url_progress.is_downloaded
        assert url_progress.summary_size == total_size
        assert url_progress.downloaded_size == downloaded_size

    def test_if_url_is_not_in_process_exception_is_raised(self, content_observer):
        with pytest.raises(URLDataException):
            content_observer.get_url_content_summary_size('/')
