"""This module contains the PluginWrapper class."""
# pylint: disable=invalid-name
from typing import Any, Dict, Generic, TypeVar, Union, cast

from polywrap_core import (
    GetFileOptions,
    InvocableResult,
    InvokeOptions,
    Invoker,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_decode
from polywrap_result import Err, Ok, Result

from .module import PluginModule

TConfig = TypeVar("TConfig")
TResult = TypeVar("TResult")


class PluginWrapper(Wrapper, Generic[TConfig]):
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
        self, options: InvokeOptions, invoker: Invoker
    ) -> Result[InvocableResult]:
        """Invoke a method on the plugin.

        Args:
            options (InvokeOptions): options to use when invoking the plugin.
            invoker (Invoker): the invoker to use when invoking the plugin.

        Returns:
            Result[InvocableResult]: the result of the invocation.
        """
        env = options.env or {}
        self.module.set_env(env)

        args: Union[Dict[str, Any], bytes] = options.args or {}
        decoded_args: Dict[str, Any] = (
            msgpack_decode(args) if isinstance(args, (bytes, bytearray)) else args
        )

        result = cast(
            Result[TResult],
            await self.module.__wrap_invoke__(options.method, decoded_args, invoker),
        )

        if result.is_err():
            return cast(Err, result)
        return Ok(InvocableResult(result=result.unwrap(), encoded=False))

    async def get_file(self, options: GetFileOptions) -> Result[Union[str, bytes]]:
        """Get a file from the plugin.

        Args:
            options (GetFileOptions): options to use when getting the file.

        Returns:
            Result[Union[str, bytes]]: the file contents or an error.
        """
        return Err.with_tb(
            RuntimeError("client.get_file(..) is not implemented for plugins")
        )

    def get_manifest(self) -> Result[AnyWrapManifest]:
        """Get the manifest of the plugin.

        Returns:
            Result[AnyWrapManifest]: the manifest of the plugin.
        """
        return Ok(self.manifest)
