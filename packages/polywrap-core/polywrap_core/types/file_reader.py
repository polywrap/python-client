from __future__ import annotations

from abc import ABC, abstractmethod

from polywrap_result import Result


class IFileReader(ABC):
    @abstractmethod
    async def read_file(self, file_path: str) -> Result[bytes]:
        pass
