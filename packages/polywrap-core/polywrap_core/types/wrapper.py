"""This module contains the Wrapper interface."""
from abc import abstractmethod
from typing import Any, Dict, Union

from polywrap_manifest import AnyWrapManifest
from polywrap_result import Result

from .invoke import Invocable, InvokeOptions, Invoker
from .options import GetFileOptions


class Wrapper(Invocable):
    """Defines the interface for a wrapper."""

    @abstractmethod
    async def invoke(self, options: InvokeOptions, invoker: Invoker) -> Result[Any]:
        """Invoke the wrapper.

        Args:
            options: The options for invoking the wrapper.
            invoker: The invoker to use for invoking the wrapper.

        Returns:
            Result[Any]: The result of invoking the wrapper or an error.
        """

    @abstractmethod
    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        """Get a file from the wrapper.

        Args:
            options: The options for getting the file.

        Returns:
            Result[Union[str, bytes]]: The file contents or an error.
        """

    @abstractmethod
    def get_manifest(self) -> Result[AnyWrapManifest]:
        """Get the manifest of the wrapper.

        Returns:
            Result[AnyWrapManifest]: The manifest or an error.
        """


WrapperCache = Dict[str, Wrapper]
