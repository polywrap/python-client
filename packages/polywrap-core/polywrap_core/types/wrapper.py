"""This module contains the Wrapper interface."""
from __future__ import annotations

from typing import Optional, Protocol, Union

from polywrap_manifest import AnyWrapManifest

from .invocable import Invocable


class Wrapper(Invocable, Protocol):
    """Defines the Wrapper protocol that extends the Invocable."""

    def get_file(
        self, path: str, encoding: Optional[str] = "utf-8"
    ) -> Union[str, bytes]:
        """Get a file from the wrapper.

        Args:
            path (str): Path to the file.
            encoding (Optional[str]): Encoding of the file.

        Returns:
            Union[str, bytes]: The file contents
        """
        ...

    def get_manifest(self) -> AnyWrapManifest:
        """Get the manifest of the wrapper.

        Returns:
            AnyWrapManifest: The manifest of the wrapper.
        """
        ...


__all__ = ["Wrapper"]
