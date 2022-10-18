from typing import Optional, Union

from polywrap_core import IFileReader, IWasmPackage, Wrapper

from .constants import WRAP_MODULE_PATH
from .inmemory_file_reader import InMemoryFileReader
from .wasm_wrapper import WasmWrapper


class WasmPackage(IWasmPackage):
    file_reader: IFileReader
    wasm_module: Optional[bytearray]

    def __init__(
        self, file_reader: IFileReader, wasm_module: Optional[bytearray] = None
    ):
        self.wasm_module = wasm_module
        self.file_reader = (
            InMemoryFileReader(wasm_module=wasm_module, base_file_reader=file_reader)
            if wasm_module
            else file_reader
        )

    async def get_wasm_module(self) -> bytearray:
        wasm_module: bytearray = self.wasm_module or await self.file_reader.read_file(
            WRAP_MODULE_PATH
        )
        self.wasm_module = wasm_module
        return wasm_module

    def create_wrapper(self) -> Wrapper:
        return WasmWrapper(self.file_reader, self.wasm_module)
