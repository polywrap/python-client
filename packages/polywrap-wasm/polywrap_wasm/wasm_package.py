from typing import Optional, Union

from polywrap_core import IFileReader, IWasmPackage, Wrapper, GetManifestOptions
from polywrap_manifest import AnyWrapManifest, deserialize_wrap_manifest

from .constants import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH
from .inmemory_file_reader import InMemoryFileReader
from .wasm_wrapper import WasmWrapper


class WasmPackage(IWasmPackage):
    file_reader: IFileReader
    manifest: Optional[Union[bytes, AnyWrapManifest]]
    wasm_module: Optional[bytes]

    def __init__(
        self, file_reader: IFileReader, manifest: Optional[Union[bytes, AnyWrapManifest]] = None, wasm_module: Optional[bytes] = None
    ):
        self.manifest = manifest
        self.wasm_module = wasm_module
        self.file_reader = (
            InMemoryFileReader(wasm_module=wasm_module, base_file_reader=file_reader)
            if wasm_module
            else file_reader
        )

    async def get_manifest(self, options: Optional[GetManifestOptions] = None) -> AnyWrapManifest:
        if self.manifest is None or isinstance(self.manifest, bytes):
            encoded_manifest = self.manifest or await self.file_reader.read_file(WRAP_MANIFEST_PATH)
            return deserialize_wrap_manifest(encoded_manifest, options)
        return self.manifest

    async def get_wasm_module(self) -> bytes:
        wasm_module: bytes = self.wasm_module or await self.file_reader.read_file(
            WRAP_MODULE_PATH
        )
        self.wasm_module = wasm_module
        return wasm_module

    async def create_wrapper(self) -> Wrapper:
        wasm_module = await self.get_wasm_module()
        wasm_manifest = await self.get_manifest() 
        return WasmWrapper(self.file_reader, wasm_module, wasm_manifest)
