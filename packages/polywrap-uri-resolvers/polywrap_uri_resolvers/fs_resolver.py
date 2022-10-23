from pathlib import Path
from polywrap_core import (
    Client,
    IFileReader,
    IUriResolutionContext,
    IUriResolver,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
)
from polywrap_wasm import WasmPackage, WRAP_MODULE_PATH, WRAP_MANIFEST_PATH
from result import Ok, Result


class SimpleFileReader(IFileReader):
    async def read_file(self, file_path: str) -> bytearray:
        with open(file_path, "rb") as f:
            return bytearray(f.read())


class FsUriResolver(IUriResolver):
    file_reader: IFileReader

    def __init__(self, file_reader: IFileReader):
        self.file_reader = file_reader

    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper, Exception]:
        if uri.authority not in ["fs", "file"]:
            return Ok(uri)

        wrapper_path = Path(uri.path)
        wasm_module = await self.file_reader.read_file(str(wrapper_path / WRAP_MODULE_PATH))
        manifest = await self.file_reader.read_file(str(wrapper_path / WRAP_MANIFEST_PATH))

        return Ok(
            UriPackage(
                uri=uri,
                package=WasmPackage(
                    wasm_module=wasm_module, manifest=manifest, file_reader=self.file_reader
                ),
            )
        )
