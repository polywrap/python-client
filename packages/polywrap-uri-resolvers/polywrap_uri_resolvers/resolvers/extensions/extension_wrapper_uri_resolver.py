"""This module contains the ExtensionWrapperUriResolver class."""
from typing import Optional, TypedDict, cast

from polywrap_core import (
    Client,
    InvokerClient,
    UriResolutionContext,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriWrapper,
    Wrapper,
    get_env_from_uri_history,
)
from polywrap_msgpack import msgpack_decode
from polywrap_wasm import WasmPackage

from ...errors import UriResolverExtensionError, UriResolverExtensionNotFoundError
from ..abc import ResolverWithHistory
from .uri_resolver_extension_file_reader import UriResolverExtensionFileReader


class MaybeUriOrManifest(TypedDict):
    """Defines a type for the return value of the extension wrapper's\
        tryResolveUri function.

    The extension wrapper's tryResolveUri function can return either a uri\
        or a manifest. This type defines the return value of the function.
    """

    uri: Optional[str]
    manifest: Optional[bytes]


class ExtensionWrapperUriResolver(ResolverWithHistory):
    """Defines a resolver that resolves a uri to a wrapper by using an extension wrapper.

    This resolver resolves a uri to a wrapper by using an extension wrapper.\
        The extension wrapper is resolved using the extension wrapper uri resolver.\
        The extension wrapper is then used to resolve the uri to a wrapper.

    Attributes:
        extension_wrapper_uri (Uri): The uri of the extension wrapper.
    """

    __slots__ = ("extension_wrapper_uri",)

    extension_wrapper_uri: Uri

    def __init__(self, extension_wrapper_uri: Uri):
        """Initialize a new ExtensionWrapperUriResolver instance.

        Args:
            extension_wrapper_uri (Uri): The uri of the extension wrapper.
        """
        self.extension_wrapper_uri = extension_wrapper_uri

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"ResolverExtension ({self.extension_wrapper_uri})"

    def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the uri using the extension wrapper.\
            If the extension wrapper returns a uri, the uri is returned.\
            If the extension wrapper returns a manifest, the manifest is used\
            to create a wrapper and the wrapper is returned.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for\
                resolving the URI.
            resolution_context (UriResolutionContext): The\
                resolution context.
        
        Returns:
            UriPackageOrWrapper: The resolved URI package, wrapper, or URI.
        """
        sub_context = resolution_context.create_sub_context()

        try:
            extension_wrapper = self._load_resolver_extension(client, sub_context)
            uri_or_manifest = self._try_resolve_uri_with_extension(
                uri, extension_wrapper, client, sub_context
            )

            if uri_or_manifest.get("uri"):
                return Uri.from_str(cast(str, uri_or_manifest["uri"]))

            if uri_or_manifest.get("manifest"):
                package = WasmPackage(
                    UriResolverExtensionFileReader(
                        self.extension_wrapper_uri, uri, client
                    ),
                    uri_or_manifest["manifest"],
                )
                return UriPackage(uri, package)

            return uri

        except Exception as err:
            raise UriResolverExtensionError(
                f"Failed to resolve uri: {uri}, using extension resolver: "
                f"({self.extension_wrapper_uri})"
            ) from err

    def _load_resolver_extension(
        self,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> Wrapper:
        """Load the URI resolver extension wrapper.

        Args:
            client (InvokerClient): The client to use for\
                resolving the URI.
            resolution_context (UriResolutionContext): The\
                resolution context.
        """
        result: UriPackageOrWrapper = client.try_resolve_uri(
            uri=self.extension_wrapper_uri, resolution_context=resolution_context
        )

        extension_wrapper: Wrapper

        if isinstance(result, UriPackage):
            extension_wrapper = result.package.create_wrapper()
        elif isinstance(result, UriWrapper):
            extension_wrapper = result.wrapper
        else:
            raise UriResolverExtensionNotFoundError(
                self.extension_wrapper_uri, resolution_context.get_history()
            )
        return extension_wrapper

    async def _try_resolve_uri_with_extension(
        self,
        uri: Uri,
        extension_wrapper: Wrapper,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> MaybeUriOrManifest:
        """Try to resolve a URI to a uri or a manifest using the extension wrapper.

        Args:
            uri (Uri): The URI to resolve.
            extension_wrapper (Wrapper): The extension wrapper.
            client (InvokerClient): The client to use for\
                resolving the URI.
            resolution_context (UriResolutionContext): The\
                resolution context.

        Returns:
            MaybeUriOrManifest: The resolved URI or manifest.
        """
        env = (
            get_env_from_uri_history(
                resolution_context.get_resolution_path(), cast(Client, client)
            )
            if hasattr(client, "get_env_by_uri")
            else None
        )

        result = extension_wrapper.invoke(
            uri=self.extension_wrapper_uri,
            method="tryResolveUri",
            args={
                "authority": uri.authority,
                "path": uri.path,
            },
            env=env,
            invoker=client,
        )

        return msgpack_decode(result.result) if result.encoded else result.result
