"""This module contains the WasmPackage type for loading a Wasm package."""
from typing import Optional, Union, cast

from polywrap_core import GetManifestOptions, IFileReader, IWasmPackage, Wrapper
from polywrap_manifest import AnyWrapManifest, deserialize_wrap_manifest
from polywrap_result import Err, Ok, Result

from .constants import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH
from .inmemory_file_reader import InMemoryFileReader
from .wasm_wrapper import WasmWrapper


class WasmPackage(IWasmPackage):
    """WasmPackage is a type that represents a Wasm WRAP package.

    Attributes:
        file_reader: The file reader used to read the package files.
        manifest: The manifest of the wrapper.
        wasm_module: The Wasm module file of the wrapper.
    """

    file_reader: IFileReader
    manifest: Optional[Union[bytes, AnyWrapManifest]]
    wasm_module: Optional[bytes]

    def __init__(
        self,
        file_reader: IFileReader,
        manifest: Optional[Union[bytes, AnyWrapManifest]] = None,
        wasm_module: Optional[bytes] = None,
    ):
        """Initialize a new WasmPackage instance."""
        self.manifest = manifest
        self.wasm_module = wasm_module
        self.file_reader = (
            InMemoryFileReader(wasm_module=wasm_module, base_file_reader=file_reader)
            if wasm_module
            else file_reader
        )

    async def get_manifest(
        self, options: Optional[GetManifestOptions] = None
    ) -> Result[AnyWrapManifest]:
        """Get the manifest of the wrapper.

        Args:
            options: The options to use when getting the manifest.
        """
        if isinstance(self.manifest, AnyWrapManifest):
            return Ok(self.manifest)

        encoded_manifest: bytes
        if self.manifest:
            encoded_manifest = self.manifest
        else:
            result = await self.file_reader.read_file(WRAP_MANIFEST_PATH)
            if result.is_err():
                return cast(Err, result)
            encoded_manifest = result.unwrap()
        deserialized_result = deserialize_wrap_manifest(encoded_manifest, options)
        if deserialized_result.is_err():
            return deserialized_result
        self.manifest = deserialized_result.unwrap()
        return Ok(self.manifest)

    async def get_wasm_module(self) -> Result[bytes]:
        """Get the Wasm module of the wrapper if it exists or return an error.

        Returns:
            The Wasm module of the wrapper or an error.
        """
        if isinstance(self.wasm_module, bytes):
            return Ok(self.wasm_module)

        result = await self.file_reader.read_file(WRAP_MODULE_PATH)
        if result.is_err():
            return cast(Err, result)
        self.wasm_module = result.unwrap()
        return Ok(self.wasm_module)

    async def create_wrapper(self) -> Result[Wrapper]:
        """Create a new WasmWrapper instance."""
        wasm_module_result = await self.get_wasm_module()
        if wasm_module_result.is_err():
            return cast(Err, wasm_module_result)
        wasm_module = wasm_module_result.unwrap()

        wasm_manifest_result = await self.get_manifest()
        if wasm_manifest_result.is_err():
            return cast(Err, wasm_manifest_result)
        wasm_manifest = wasm_manifest_result.unwrap()

        return Ok(WasmWrapper(self.file_reader, wasm_module, wasm_manifest))
