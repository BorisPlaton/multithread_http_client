import shutil
from pathlib import Path

import pytest

from http_client.utils.file_saver import FileSaver


@pytest.mark.http_client
class TestFileSaver:

    @pytest.fixture
    def file_saver(self, content_dir):
        return FileSaver(content_dir)

    @pytest.fixture
    def content(self):
        return b'some very interesting content'

    @staticmethod
    def delete_dir(path_to_dir: Path):
        try:
            shutil.rmtree(path_to_dir)
        except FileNotFoundError:
            pass

    def test_content_is_saved_to_directory(self, file_saver, content):
        file_name = 'test_file.txt'
        path_to_file = file_saver.save_content_to_file_system(content, file_name)
        path_to_saved_file = Path(path_to_file)
        assert path_to_saved_file.exists()
        with path_to_saved_file.open('rb') as f:
            assert f.read() == content

    @pytest.mark.parametrize(
        'directory_name', [
            'd', 's', 'dir'
        ]
    )
    def test_new_directory_is_created(self, directory_name, content):
        content_dir = Path(__file__).parent / directory_name
        file_saver = FileSaver(content_dir)
        file_saver.create_directory(content_dir)
        try:
            assert Path(content_dir).exists()
        finally:
            self.delete_dir(content_dir)
