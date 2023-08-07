"""This module contains the embedded file reader."""
from pathlib import Path

from polywrap_core import FileReader


class EmbeddedFileReader(FileReader):
    """A file reader that reads from the embedded files."""

    def __init__(self, embedded_wrap_path: Path):
        """Initialize the embedded file reader."""
        self._embedded_wrap_path = embedded_wrap_path

    def read_file(self, file_path: str) -> bytes:
        """Read the file from the embedded files."""
        with open(self._embedded_wrap_path / file_path, "rb") as f:
            return f.read()


__all__ = ["EmbeddedFileReader"]
