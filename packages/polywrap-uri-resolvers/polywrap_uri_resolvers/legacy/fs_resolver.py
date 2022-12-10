from pathlib import Path
from typing import cast

from polywrap_core import (
    Client,
    IFileReader,
    IUriResolutionContext,
    IUriResolver,
    Uri,
    UriPackageOrWrapper,
)
from polywrap_result import Err, Ok, Result
from polywrap_wasm import WRAP_MANIFEST_PATH, WRAP_MODULE_PATH, WasmPackage


class SimpleFileReader(IFileReader):
    async def read_file(self, file_path: str) -> Result[bytes]:
        with open(file_path, "rb") as f:
            return Ok(f.read())


class FsUriResolver(IUriResolver):
    file_reader: IFileReader

    def __init__(self, file_reader: IFileReader):
        self.file_reader = file_reader

    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        if uri.authority not in ["fs", "file"]:
            return Ok(uri)

        wrapper_path = Path(uri.path)

        wasm_module_result = await self.file_reader.read_file(
            str(wrapper_path / WRAP_MODULE_PATH)
        )
        if wasm_module_result.is_err():
            return cast(Err, wasm_module_result)
        wasm_module = wasm_module_result.unwrap()

        manifest_result = await self.file_reader.read_file(
            str(wrapper_path / WRAP_MANIFEST_PATH)
        )
        if manifest_result.is_err():
            return cast(Err, manifest_result)
        manifest = manifest_result.unwrap()

        return Ok(
            WasmPackage(
                wasm_module=wasm_module,
                manifest=manifest,
                file_reader=self.file_reader,
            )
        )
