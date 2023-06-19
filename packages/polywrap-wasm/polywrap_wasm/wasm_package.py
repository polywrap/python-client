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
    """WasmPackage implements the WRAP package protocol for a Wasm WRAP package.

    Args:
        file_reader (FileReader): The file reader used to read\
            the package files.
        manifest (Optional[Union[bytes, AnyWrapManifest]]): \
            The manifest of the wrapper.
        wasm_module (Optional[bytes]): The Wasm module file\
            of the wrapper.
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
            options (Optional[DeserializeManifestOptions]): The options\
                to use when getting the manifest.

        Returns:
            AnyWrapManifest: The manifest of the wrapper.

        Raises:
            OSError: If the manifest file could not be read due to system errors.
            MsgpackDecodeError: If the encoded manifest fails to decode.
            ManifestError: If the manifest is not valid.
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

        Raises:
            OSError: If the wasm module file could not be read due to system errors.

        Returns:
            The Wasm module of the wrapper or an error.
        """
        if isinstance(self.wasm_module, bytes):
            return self.wasm_module

        wasm_module = self.file_reader.read_file(WRAP_MODULE_PATH)
        self.wasm_module = wasm_module
        return self.wasm_module

    def create_wrapper(self) -> Wrapper:
        """Create a new WasmWrapper instance.

        Returns:
            WasmWrapper: The Wasm wrapper instance.

        Raises:
            OSError: If the wasm module or manifest could not be read\
                due to system errors.
            MsgpackDecodeError: If the encoded manifest fails to decode.
            ManifestError: If the manifest is not valid.
        """
        wasm_module = self.get_wasm_module()
        wasm_manifest = self.get_manifest()

        return WasmWrapper(self.file_reader, wasm_module, wasm_manifest)


__all__ = ["WasmPackage"]
