"""This module contains the UriResolverExtensionFileReader class."""
from pathlib import Path

from polywrap_core import FileReader, Invoker, Uri


class UriResolverExtensionFileReader(FileReader):
    """Defines a file reader that uses an extension wrapper to read files.

    This file reader uses an extension wrapper to read files.\
        The extension wrapper is used to read files by invoking the getFile method.\
        The getFile method is invoked with the path of the file to read.

    Args:
        extension_uri (Uri): The uri of the extension wrapper.
        wrapper_uri (Uri): The uri of the wrapper that uses the extension wrapper.
        invoker (Invoker): The invoker used to invoke the getFile method.
    """

    extension_uri: Uri
    """The uri of the extension wrapper."""

    wrapper_uri: Uri
    """The uri of the wrapper that uses the extension wrapper."""

    invoker: Invoker
    """The invoker used to invoke the getFile method."""

    def __init__(
        self,
        extension_uri: Uri,
        wrapper_uri: Uri,
        invoker: Invoker,
    ):
        """Initialize a new UriResolverExtensionFileReader instance."""
        self.extension_uri = extension_uri
        self.wrapper_uri = wrapper_uri
        self.invoker = invoker

    def read_file(self, file_path: str) -> bytes:
        """Read a file using the extension wrapper.

        Args:
            file_path (str): The path of the file to read.

        Returns:
            bytes: The contents of the file.
        """
        path = str(Path(self.wrapper_uri.path).joinpath(file_path))
        result = self.invoker.invoke(
            uri=self.extension_uri, method="getFile", args={"path": path}
        )

        if not isinstance(result, bytes):
            raise FileNotFoundError(
                f"File not found at path: {path}, using resolver: {self.extension_uri}"
            )
        return result


__all__ = ["UriResolverExtensionFileReader"]
