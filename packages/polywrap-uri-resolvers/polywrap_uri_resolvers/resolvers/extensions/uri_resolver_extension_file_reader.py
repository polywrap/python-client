
from pathlib import Path
from polywrap_core import FileReader, Invoker, InvokerOptions, Uri, UriPackageOrWrapper


class UriResolverExtensionFileReader(FileReader):
    extension_uri: Uri
    wrapper_uri: Uri
    invoker: Invoker[UriPackageOrWrapper]

    def __init__(self, extension_uri: Uri, wrapper_uri: Uri, invoker: Invoker[UriPackageOrWrapper]):
        self.extension_uri = extension_uri
        self.wrapper_uri = wrapper_uri
        self.invoker = invoker

    async def read_file(self, file_path: str) -> bytes:
        path = str(Path(self.wrapper_uri.path).joinpath(file_path))
        result = await self.invoker.invoke(
            InvokerOptions(uri=self.extension_uri, method="getFile", args={"path": path})
        )

        if not isinstance(result, bytes):
            raise FileNotFoundError(f"File not found at path: {path}, using resolver: {self.extension_uri}")
        return result
