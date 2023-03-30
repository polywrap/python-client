"""This module contains the FS URI resolver."""
from pathlib import Path

from polywrap_core import (
    FileReader,
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolver,
)
from polywrap_wasm import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH, WasmPackage


class SimpleFileReader(FileReader):
    """Defines a simple file reader."""

    async def read_file(self, file_path: str) -> bytes:
        """Read a file.

        Args:
            file_path (str): The path of the file to read.

        Returns:
            bytes: The contents of the file.
        """
        with open(file_path, "rb") as f:
            return f.read()


class FsUriResolver(UriResolver):
    """Defines a URI resolver that resolves file system URIs."""

    file_reader: FileReader

    def __init__(self, file_reader: FileReader):
        """Initialize a new FsUriResolver instance.

        Args:
            file_reader (FileReader): The file reader used to read files.
        """
        self.file_reader = file_reader

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The resolution context.

        Returns:
            UriPackageOrWrapper: The resolved URI.
        """
        if uri.authority not in ["fs", "file"]:
            return uri

        wrapper_path = Path(uri.path)

        wasm_module = await self.file_reader.read_file(
            str(wrapper_path / WRAP_MODULE_PATH)
        )

        manifest = await self.file_reader.read_file(
            str(wrapper_path / WRAP_MANIFEST_PATH)
        )

        return UriPackage(
            uri=uri,
            package=WasmPackage(
                wasm_module=wasm_module,
                manifest=manifest,
                file_reader=self.file_reader,
            ),
        )
