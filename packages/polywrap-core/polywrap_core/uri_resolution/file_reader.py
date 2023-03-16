"""This module contains file reader interface."""
from __future__ import annotations

from abc import ABC, abstractmethod

from polywrap_result import Result


class IFileReader(ABC):
    """File reader interface."""

    @abstractmethod
    async def read_file(self, file_path: str) -> Result[bytes]:
        """Read a file from the given file path.

        Args:
            file_path: The path of the file to read.

        Returns:
            Result[bytes]: The file contents or an error.
        """
