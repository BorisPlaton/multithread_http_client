import os
from pathlib import Path
from uuid import uuid4


class FileSaver:
    """Saves content in bytes to the file in a specific directory."""

    def save_content_to_file_system(self, content: bytes, filename: str = None) -> str:
        """Creates a new file and writes all given content to it."""
        filename = filename if isinstance(filename, str) else str(uuid4())
        path_to_file = self.files_directory / filename
        try:
            with open(path_to_file, 'wb') as f:
                f.write(content)
        except FileNotFoundError:
            self.create_directory(self.files_directory)
            return self.save_content_to_file_system(content, filename)
        return str(path_to_file.as_uri())

    @staticmethod
    def create_directory(directory_path: Path):
        """Creates a directory with given path."""
        os.mkdir(directory_path)

    def __init__(self, files_directory: Path):
        """
        Saves a path to the directory where all files will be
        saved.
        """
        self.files_directory = files_directory
