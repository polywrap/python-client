"""This module contains file reader interface."""
from __future__ import annotations

from typing import Protocol


class FileReader(Protocol):
    """Defines the FileReader protocol used by UriResolver."""

    def read_file(self, file_path: str) -> bytes:
        """Read a file from the given file path.

        Args:
            file_path: The path of the file to read.

        Raises:
            OSError: If the file could not be read due to system errors.

        Returns:
            bytes: The file contents.
        """
        ...


__all__ = ["FileReader"]
