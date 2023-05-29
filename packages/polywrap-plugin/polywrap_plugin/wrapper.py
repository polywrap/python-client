"""This module contains the PluginWrapper class."""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
from typing import Any, Generic, Optional, TypeVar, Union

from polywrap_core import InvocableResult, InvokerClient, Uri, UriResolutionContext, Wrapper
from polywrap_manifest import AnyWrapManifest

from .module import InvokeOptions, PluginModule
from .resolution_context_override_client import ResolutionContextOverrideClient

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

    def invoke(
        self,
        uri: Uri,
        method: str,
        args: Optional[Any] = None,
        env: Optional[Any] = None,
        resolution_context: Optional[UriResolutionContext] = None,
        client: Optional[InvokerClient] = None,
    ) -> InvocableResult:
        """Invoke the Wrapper based on the provided InvokeOptions.

        Args:
            uri (Uri): Uri of the wrapper
            method (str): Method to be executed
            args (Optional[Any]) : Arguments for the method, structured as a dictionary
            env (Optional[Any]): Override the client's config for all invokes within this invoke.
            resolution_context (Optional[UriResolutionContext]): A URI resolution context
            client (Optional[Invoker]): The invoker instance requesting this invocation.\
                This invoker will be used for any subinvocation that may occur.

        Returns:
            InvocableResult: Result of the invocation.
        """
        options = InvokeOptions(
            uri=uri,
            method=method,
            args=args,
            env=env,
            resolution_context=resolution_context,
            client=ResolutionContextOverrideClient(client, resolution_context)
            if client
            else None,
        )
        result = self.module.__wrap_invoke__(options)
        return InvocableResult(result=result, encoded=False)

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
        raise NotImplementedError("client.get_file(..) is not implemented for plugins")

    def get_manifest(self) -> AnyWrapManifest:
        """Get the manifest of the plugin.

        Returns:
            Result[AnyWrapManifest]: the manifest of the plugin.
        """
        return self.manifest


__all__ = ["PluginWrapper"]
