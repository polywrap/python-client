"""This module contains the Polywrap client implementation."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from polywrap_core import (
    Client,
    ClientConfig,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriResolver,
    UriWrapper,
    Wrapper,
    get_env_from_resolution_path,
)
from polywrap_core import get_implementations as core_get_implementations
from polywrap_manifest import AnyWrapManifest, DeserializeManifestOptions
from polywrap_msgpack import msgpack_decode, msgpack_encode

from polywrap_client.errors import WrapNotFoundError


class PolywrapClient(Client):
    """Defines the Polywrap client.

    Args:
        config (ClientConfig): The polywrap client config.
    """

    _config: ClientConfig

    def __init__(self, config: ClientConfig):
        """Initialize a new PolywrapClient instance."""
        self._config = config

    def get_config(self) -> ClientConfig:
        """Get the client configuration.

        Returns:
            ClientConfig: The polywrap client configuration.
        """
        return self._config

    def get_uri_resolver(self) -> UriResolver:
        """Get the URI resolver.

        Returns:
            UriResolver: The URI resolver.
        """
        return self._config.resolver

    def get_envs(self) -> Dict[Uri, Any]:
        """Get the dictionary of environment variables.

        Returns:
            Dict[Uri, Any]: The dictionary of environment variables.
        """
        envs: Dict[Uri, Any] = self._config.envs
        return envs

    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        """Get the interfaces.

        Returns:
            Dict[Uri, List[Uri]]: The dictionary of interface-implementations.
        """
        interfaces: Dict[Uri, List[Uri]] = self._config.interfaces
        return interfaces

    def get_implementations(
        self,
        uri: Uri,
        apply_resolution: bool = True,
        resolution_context: Optional[UriResolutionContext] = None,
    ) -> Optional[List[Uri]]:
        """Get implementations of an interface with its URI.

        Args:
            uri (Uri): URI of the interface.
            apply_resolution (bool): If True, apply resolution to the URI and interfaces.
            resolution_context (Optional[UriResolutionContext]): A URI resolution context

        Returns:
            Optional[List[Uri]]: List of implementations or None if not found.

        Raises:
            WrapGetImplementationsError: If the URI cannot be resolved.
        """
        interfaces: Dict[Uri, List[Uri]] = self.get_interfaces()
        if not apply_resolution:
            return interfaces.get(uri)

        return core_get_implementations(uri, interfaces, self, resolution_context)

    def get_env_by_uri(self, uri: Uri) -> Union[Any, None]:
        """Get the environment variables for the given URI.

        Args:
            uri (Uri): The URI of the wrapper.

        Returns:
            Union[Any, None]: The environment variables.
        """
        return self._config.envs.get(uri)

    def get_file(
        self, uri: Uri, path: str, encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
        """Get the file from the given wrapper URI.

        Args:
            uri (Uri): The wrapper URI.
            path (str): The path to the file.
            encoding (Optional[str]): The encoding of the file.

        Returns:
            Union[bytes, str]: The file contents.
        """
        loaded_wrapper = self.load_wrapper(uri)
        return loaded_wrapper.get_file(path, encoding)

    def get_manifest(
        self, uri: Uri, options: Optional[DeserializeManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get the manifest from the given wrapper URI.

        Args:
            uri (Uri): The wrapper URI.
            options (Optional[DeserializeManifestOptions]): The manifest options.

        Returns:
            AnyWrapManifest: The manifest.
        """
        loaded_wrapper = self.load_wrapper(uri)
        return loaded_wrapper.get_manifest()

    def try_resolve_uri(
        self, uri: Uri, resolution_context: Optional[UriResolutionContext] = None
    ) -> UriPackageOrWrapper:
        """Try to resolve the given URI.

        Args:
            uri (Uri): The URI to resolve.
            resolution_context (Optional[UriResolutionContext]):\
                The resolution context.

        Returns:
            UriPackageOrWrapper: The resolved URI, package or wrapper.

        Raises:
            UriResolutionError: If the URI cannot be resolved.
        """
        uri_resolver = self._config.resolver
        resolution_context = resolution_context or UriResolutionContext()

        return uri_resolver.try_resolve_uri(uri, self, resolution_context)

    def load_wrapper(
        self,
        uri: Uri,
        resolution_context: Optional[UriResolutionContext] = None,
    ) -> Wrapper:
        """Load the wrapper for the given URI.

        Args:
            uri (Uri): The wrapper URI.
            resolution_context (Optional[UriResolutionContext]):\
                The resolution context.

        Returns:
            Wrapper: initialized wrapper instance.

        Raises:
            UriResolutionError: If the URI cannot be resolved.
            WrapNotFoundError: If the wrap is not found.
        """
        resolution_context = resolution_context or UriResolutionContext()
        uri_package_or_wrapper = self.try_resolve_uri(
            uri=uri, resolution_context=resolution_context
        )

        match uri_package_or_wrapper:
            case UriPackage(uri=uri, package=package):
                return package.create_wrapper()
            case UriWrapper(uri=uri, wrapper=wrapper):
                return wrapper
            case _:
                raise WrapNotFoundError(uri=uri, resolution_context=resolution_context)

    def invoke(
        self,
        uri: Uri,
        method: str,
        args: Optional[Any] = None,
        env: Optional[Any] = None,
        resolution_context: Optional[UriResolutionContext] = None,
        encode_result: Optional[bool] = False,
    ) -> Any:
        """Invoke the given wrapper URI.

        Args:
            uri (Uri): The wrapper URI.
            method (str): The method to invoke.
            args (Optional[Any]): The arguments to pass to the method.
            env (Optional[Any]): The environment variables to pass.
            resolution_context (Optional[UriResolutionContext]):\
                The resolution context.
            encode_result (Optional[bool]): If True, encode the result.

        Returns:
            Any: The result of the invocation.

        Raises:
            MsgpackError: If the data cannot be encoded/decoded.
            ManifestError: If the manifest is invalid.
            WrapError: If something went wrong during the invocation.
            WrapNotFoundError: If the wrap is not found.
            UriResolutionError: If the URI cannot be resolved.
        """
        resolution_context = resolution_context or UriResolutionContext()
        load_wrapper_context = resolution_context.create_sub_history_context()
        wrapper = self.load_wrapper(uri, resolution_context=load_wrapper_context)
        wrapper_resolution_path = load_wrapper_context.get_resolution_path()
        wrapper_resolved_uri = wrapper_resolution_path[-1]

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=UriWrapper(uri=uri, wrapper=wrapper),
                description="Client.load_wrapper",
                sub_history=load_wrapper_context.get_history(),
            )
        )

        env = env or get_env_from_resolution_path(
            load_wrapper_context.get_resolution_path(), self
        )

        wrapper_invoke_context = resolution_context.create_sub_history_context()

        invocable_result = wrapper.invoke(
            uri=wrapper_resolved_uri,
            method=method,
            args=args,
            env=env,
            resolution_context=wrapper_invoke_context,
            client=self,
        )

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=wrapper_resolved_uri,
                result=wrapper_resolved_uri,
                description="Wrapper.invoke",
                sub_history=wrapper_invoke_context.get_history(),
            )
        )

        if encode_result and not invocable_result.encoded:
            encoded = msgpack_encode(invocable_result.result)
            return encoded

        if (
            not encode_result
            and invocable_result.encoded
            and isinstance(invocable_result.result, (bytes, bytearray))
        ):
            decoded: Any = msgpack_decode(invocable_result.result)
            return decoded

        return invocable_result.result


__all__ = ["PolywrapClient"]
