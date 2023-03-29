from pathlib import Path

from polywrap_core import (
    InvokerClient,
    IFileReader,
    IUriResolutionContext,
    UriResolver,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
)
from polywrap_wasm import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH, WasmPackage


class SimpleFileReader(IFileReader):
    async def read_file(self, file_path: str) -> bytes:
        with open(file_path, "rb") as f:
            return f.read()


class FsUriResolver(UriResolver):
    file_reader: IFileReader

    def __init__(self, file_reader: IFileReader):
        self.file_reader = file_reader

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
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
