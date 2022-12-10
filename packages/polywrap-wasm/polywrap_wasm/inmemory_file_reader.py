from typing import Optional

from polywrap_core import IFileReader
from polywrap_result import Ok, Result

from .constants import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH


class InMemoryFileReader(IFileReader):
    _wasm_manifest: Optional[bytes]
    _wasm_module: Optional[bytes]
    _base_file_reader: IFileReader

    def __init__(
        self,
        base_file_reader: IFileReader,
        wasm_module: Optional[bytes] = None,
        wasm_manifest: Optional[bytes] = None,
    ):
        self._wasm_module = wasm_module
        self._wasm_manifest = wasm_manifest
        self._base_file_reader = base_file_reader

    async def read_file(self, file_path: str) -> Result[bytes]:
        if file_path == WRAP_MODULE_PATH and self._wasm_module:
            return Ok(self._wasm_module)
        elif file_path == WRAP_MANIFEST_PATH and self._wasm_manifest:
            return Ok(self._wasm_manifest)
        else:
            return await self._base_file_reader.read_file(file_path=file_path)
