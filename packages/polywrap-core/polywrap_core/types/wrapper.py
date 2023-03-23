"""This module contains the Wrapper interface."""
from abc import abstractmethod
from typing import Any, Dict, Generic, TypeVar, Union

from polywrap_manifest import AnyWrapManifest

from .invocable import Invocable
from .invoker import InvokeOptions, Invoker
from .options import GetFileOptions
from .uri_like import UriLike

T = TypeVar("T", bound=UriLike)


class Wrapper(Generic[T], Invocable[T]):
    """Defines the interface for a wrapper."""

    @abstractmethod
    async def invoke(self, options: InvokeOptions[T], invoker: Invoker[T]) -> Any:
        """Invoke the wrapper.

        Args:
            options: The options for invoking the wrapper.
            invoker: The invoker to use for invoking the wrapper.

        Returns:
            Any: The result of the wrapper invocation.
        """

    @abstractmethod
    async def get_file(self, options: GetFileOptions) -> Union[str, bytes]:
        """Get a file from the wrapper.

        Args:
            options: The options for getting the file.

        Returns:
            Union[str, bytes]: The file contents
        """

    @abstractmethod
    def get_manifest(self) -> AnyWrapManifest:
        """Get the manifest of the wrapper.

        Returns:
            AnyWrapManifest: The manifest of the wrapper.
        """


WrapperCache = Dict[str, Wrapper[T]]
