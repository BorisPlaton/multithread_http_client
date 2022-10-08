import pytest

from http_client.models.storages.structs import DownloadedContent, InProcessURLData


@pytest.mark.http_client
class TestDownloadedContentStruct:

    @pytest.fixture
    def downloaded_content(self):
        return DownloadedContent(b'123456789', byte_range_start=0)

    def test_content_size_is_correct(self):
        content = DownloadedContent(b'123456789', byte_range_start=0)
        assert content.size == 9

    def test_content_size_is_cachable(self, downloaded_content):
        assert 'size' not in vars(downloaded_content)
        downloaded_content.size
        assert 'size' in vars(downloaded_content)


@pytest.mark.http_client
class TestInProcessURLDataStruct:

    @pytest.fixture
    def in_process_url(self):
        return InProcessURLData('/', 1000)

    @pytest.fixture
    def downloaded_content(self):
        return DownloadedContent(b'123456789', byte_range_start=0)

    def test_struct_can_be_created(self):
        in_process = InProcessURLData('/', 10)
        assert in_process
        in_process = InProcessURLData('/', 10, [])
        assert in_process

    def test_only_downloaded_content_can_be_added_to_struct(self, in_process_url, downloaded_content):
        assert not in_process_url.downloaded_fragments
        in_process_url.add_downloaded_fragment(downloaded_content)
        assert in_process_url.downloaded_fragments

    @pytest.mark.parametrize(
        'wrong_value',
        [dict, 1, '2', DownloadedContent, InProcessURLData]
    )
    def test_exception_raised_if_wrong_downloaded_content_added(self, in_process_url, wrong_value):
        assert not in_process_url.downloaded_fragments
        with pytest.raises(ValueError):
            in_process_url.add_downloaded_fragment(wrong_value)

    def test_downloaded_content_size_is_evaluated_correct(self, in_process_url):
        downloaded_fragments = [
            DownloadedContent(b'123456789', byte_range_start=0),
            DownloadedContent(b'12345', byte_range_start=0),
            DownloadedContent(b'1234567', byte_range_start=0),
            DownloadedContent(b'12', byte_range_start=0),
        ]
        for fragment in downloaded_fragments:
            in_process_url.add_downloaded_fragment(fragment)
        assert in_process_url.downloaded_content_size == 23

    def test_progress_is_evaluated_correct(self):
        in_process = InProcessURLData('/', 100)
        downloaded_fragments = [
            DownloadedContent(b'12345', byte_range_start=0),
            DownloadedContent(b'12345', byte_range_start=0),
            DownloadedContent(b'12345', byte_range_start=0),
            DownloadedContent(b'12', byte_range_start=0),
        ]

        for fragment in downloaded_fragments:
            in_process.add_downloaded_fragment(fragment)
        assert in_process.progress == 17

    def test_progress_has_two_digit_after_comma(self):
        in_process = InProcessURLData('/', 24)
        downloaded_fragments = [
            DownloadedContent(b'12345', byte_range_start=0),
            DownloadedContent(b'12345', byte_range_start=0),
            DownloadedContent(b'12345', byte_range_start=0),
            DownloadedContent(b'12', byte_range_start=0),
        ]
        for fragment in downloaded_fragments:
            in_process.add_downloaded_fragment(fragment)
        assert len(str(in_process.progress).split('.')[1]) == 2
