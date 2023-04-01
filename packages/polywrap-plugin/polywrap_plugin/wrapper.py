"""This module contains the PluginWrapper class."""
# pylint: disable=invalid-name
from typing import Generic, TypeVar, Union

from polywrap_core import (
    GetFileOptions,
    InvocableResult,
    InvokeOptions,
    Invoker,
    UriPackageOrWrapper,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest

from .module import PluginModule

TConfig = TypeVar("TConfig")
TResult = TypeVar("TResult")


class PluginWrapper(Generic[TConfig], Wrapper[UriPackageOrWrapper]):
    """PluginWrapper implements the Wrapper interface for plugin wrappers.

    Attributes:
        module: The plugin module.
        manifest: The manifest of the plugin.
    """

    module: PluginModule[TConfig]
    manifest: AnyWrapManifest

    def __init__(
        self, module: PluginModule[TConfig], manifest: AnyWrapManifest
    ) -> None:
        """Initialize a new PluginWrapper instance.

        Args:
            module: The plugin module.
            manifest: The manifest of the plugin.
        """
        self.module = module
        self.manifest = manifest

    async def invoke(
        self,
        options: InvokeOptions[UriPackageOrWrapper],
        invoker: Invoker[UriPackageOrWrapper],
    ) -> InvocableResult:
        """Invoke a method on the plugin.

        Args:
            options (InvokeOptions): options to use when invoking the plugin.
            invoker (Invoker): the invoker to use when invoking the plugin.

        Returns:
            Result[InvocableResult]: the result of the invocation.
        """
        result = await self.module.__wrap_invoke__(options, invoker)
        return InvocableResult(result=result, encoded=False)

    async def get_file(self, options: GetFileOptions) -> Union[str, bytes]:
        """Get a file from the plugin.

        Args:
            options (GetFileOptions): options to use when getting the file.

        Returns:
            Result[Union[str, bytes]]: the file contents or an error.
        """
        raise NotImplementedError("client.get_file(..) is not implemented for plugins")

    def get_manifest(self) -> AnyWrapManifest:
        """Get the manifest of the plugin.

        Returns:
            Result[AnyWrapManifest]: the manifest of the plugin.
        """
        return self.manifest
