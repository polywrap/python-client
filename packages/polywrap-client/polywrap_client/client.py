"""This module contains the Polywrap client implementation."""
from __future__ import annotations

import json
from textwrap import dedent
from typing import Any, Dict, List, Optional, Union, cast

from polywrap_core import (
    Client,
    ClientConfig,
    Env,
    GetFileOptions,
    GetManifestOptions,
    InvokerOptions,
    IUriResolutionContext,
    TryResolveUriOptions,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolver,
    UriWrapper,
    Wrapper,
)
from polywrap_manifest import AnyWrapManifest
from polywrap_msgpack import msgpack_decode, msgpack_encode
from polywrap_uri_resolvers import UriResolutionContext, build_clean_uri_history


class PolywrapClient(Client):
    """Defines the Polywrap client.

    Attributes:
        _config (ClientConfig): The client configuration.
    """

    _config: ClientConfig

    def __init__(self, config: ClientConfig):
        """Initialize a new PolywrapClient instance.

        Args:
            config (ClientConfig): The polywrap client config.
        """
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

    def get_envs(self) -> Dict[Uri, Env]:
        """Get the dictionary of environment variables.

        Returns:
            Dict[Uri, Env]: The dictionary of environment variables.
        """
        envs: Dict[Uri, Env] = self._config.envs
        return envs

    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        """Get the interfaces.

        Returns:
            Dict[Uri, List[Uri]]: The dictionary of interface-implementations.
        """
        interfaces: Dict[Uri, List[Uri]] = self._config.interfaces
        return interfaces

    def get_implementations(self, uri: Uri) -> Union[List[Uri], None]:
        """Get the implementations for the given interface URI.

        Args:
            uri (Uri): The interface URI.

        Returns:
            Union[List[Uri], None]: The list of implementation URIs.
        """
        interfaces: Dict[Uri, List[Uri]] = self.get_interfaces()
        return interfaces.get(uri)

    def get_env_by_uri(self, uri: Uri) -> Union[Env, None]:
        """Get the environment variables for the given URI.

        Args:
            uri (Uri): The URI of the wrapper.

        Returns:
            Union[Env, None]: The environment variables.
        """
        return self._config.envs.get(uri)

    async def get_file(self, uri: Uri, options: GetFileOptions) -> Union[bytes, str]:
        """Get the file from the given wrapper URI.

        Args:
            uri (Uri): The wrapper URI.
            options (GetFileOptions): The options for getting the file.

        Returns:
            Union[bytes, str]: The file contents.
        """
        loaded_wrapper = await self.load_wrapper(uri)
        return await loaded_wrapper.get_file(options)

    async def get_manifest(
        self, uri: Uri, options: Optional[GetManifestOptions] = None
    ) -> AnyWrapManifest:
        """Get the manifest from the given wrapper URI.

        Args:
            uri (Uri): The wrapper URI.
            options (Optional[GetManifestOptions]): The options for getting the manifest.

        Returns:
            AnyWrapManifest: The manifest.
        """
        loaded_wrapper = await self.load_wrapper(uri)
        return loaded_wrapper.get_manifest()

    async def try_resolve_uri(
        self, options: TryResolveUriOptions[UriPackageOrWrapper]
    ) -> UriPackageOrWrapper:
        """Try to resolve the given URI.

        Args:
            options (TryResolveUriOptions[UriPackageOrWrapper]): The options for resolving the URI.

        Returns:
            UriPackageOrWrapper: The resolved URI, package or wrapper.
        """
        uri = options.uri
        uri_resolver = self._config.resolver
        resolution_context = options.resolution_context or UriResolutionContext()

        return await uri_resolver.try_resolve_uri(uri, self, resolution_context)

    async def load_wrapper(
        self,
        uri: Uri,
        resolution_context: Optional[IUriResolutionContext[UriPackageOrWrapper]] = None,
    ) -> Wrapper[UriPackageOrWrapper]:
        """Load the wrapper for the given URI.

        Args:
            uri (Uri): The wrapper URI.
            resolution_context (Optional[IUriResolutionContext[UriPackageOrWrapper]]):\
                The resolution context.

        Returns:
            Wrapper[UriPackageOrWrapper]: initialized wrapper instance.
        """
        resolution_context = resolution_context or UriResolutionContext()

        uri_package_or_wrapper = await self.try_resolve_uri(
            TryResolveUriOptions(uri=uri, resolution_context=resolution_context)
        )

        if isinstance(uri_package_or_wrapper, UriPackage):
            return await cast(
                UriPackage[UriPackageOrWrapper], uri_package_or_wrapper
            ).package.create_wrapper()

        if isinstance(uri_package_or_wrapper, UriWrapper):
            return cast(UriWrapper[UriPackageOrWrapper], uri_package_or_wrapper).wrapper

        raise RuntimeError(
            dedent(
                f"""
                Error resolving URI "{uri.uri}"
                URI not found
                Resolution Stack: {
                    json.dumps(
                        build_clean_uri_history(
                            resolution_context.get_history()
                        ), indent=2
                    )
                }
                """
            )
        )

    async def invoke(self, options: InvokerOptions[UriPackageOrWrapper]) -> Any:
        """Invoke the given wrapper URI.

        Args:
            options (InvokerOptions[UriPackageOrWrapper]): The options for invoking the wrapper.

        Returns:
            Any: The result of the invocation.
        """
        resolution_context = options.resolution_context or UriResolutionContext()
        wrapper = await self.load_wrapper(
            options.uri, resolution_context=resolution_context
        )
        options.env = options.env or self.get_env_by_uri(options.uri)

        invocable_result = await wrapper.invoke(options, invoker=self)

        if options.encode_result and not invocable_result.encoded:
            encoded = msgpack_encode(invocable_result.result)
            return encoded

        if (
            not options.encode_result
            and invocable_result.encoded
            and isinstance(invocable_result.result, (bytes, bytearray))
        ):
            decoded: Any = msgpack_decode(invocable_result.result)
            return decoded

        return invocable_result.result
