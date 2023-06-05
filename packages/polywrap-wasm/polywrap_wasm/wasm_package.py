"""This module contains the WasmPackage type for loading a Wasm package."""
from typing import Optional, Union

from polywrap_core import FileReader, WrapPackage, Wrapper
from polywrap_manifest import (
    AnyWrapManifest,
    DeserializeManifestOptions,
    deserialize_wrap_manifest,
)

from .constants import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH
from .inmemory_file_reader import InMemoryFileReader
from .wasm_wrapper import WasmWrapper


class WasmPackage(WrapPackage):
    """WasmPackage is a type that represents a Wasm WRAP package.

    Attributes:
        file_reader: The file reader used to read the package files.
        manifest: The manifest of the wrapper.
        wasm_module: The Wasm module file of the wrapper.
    """

    file_reader: FileReader
    manifest: Optional[Union[bytes, AnyWrapManifest]]
    wasm_module: Optional[bytes]

    def __init__(
        self,
        file_reader: FileReader,
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

    def get_manifest(
        self, options: Optional[DeserializeManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get the manifest of the wrapper.

        Args:
            options: The options to use when getting the manifest.
        """
        if isinstance(self.manifest, AnyWrapManifest):
            return self.manifest

        encoded_manifest = self.manifest or self.file_reader.read_file(
            WRAP_MANIFEST_PATH
        )
        manifest = deserialize_wrap_manifest(encoded_manifest, options)
        return manifest

    def get_wasm_module(self) -> bytes:
        """Get the Wasm module of the wrapper if it exists or return an error.

        Returns:
            The Wasm module of the wrapper or an error.
        """
        if isinstance(self.wasm_module, bytes):
            return self.wasm_module

        wasm_module = self.file_reader.read_file(WRAP_MODULE_PATH)
        self.wasm_module = wasm_module
        return self.wasm_module

    def create_wrapper(self) -> Wrapper:
        """Create a new WasmWrapper instance."""
        wasm_module = self.get_wasm_module()
        wasm_manifest = self.get_manifest()

        return WasmWrapper(self.file_reader, wasm_module, wasm_manifest)


__all__ = ["WasmPackage"]
