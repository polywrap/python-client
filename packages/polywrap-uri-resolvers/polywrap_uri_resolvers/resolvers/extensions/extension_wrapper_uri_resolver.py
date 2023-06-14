"""This module contains the ExtensionWrapperUriResolver class."""
from __future__ import annotations

from typing import Optional, TypedDict

from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriResolver,
    WrapError,
)
from polywrap_wasm import WasmPackage

from ...errors import (
    InfiniteLoopError,
    UriResolverExtensionError,
    UriResolverExtensionNotFoundError,
)
from .uri_resolver_extension_file_reader import UriResolverExtensionFileReader


class MaybeUriOrManifest(TypedDict, total=False):
    """Defines a type for the return value of the extension wrapper's\
        tryResolveUri function.

    The extension wrapper's tryResolveUri function can return either a uri\
        or a manifest. This type defines the return value of the function.
    """

    uri: Optional[str]
    manifest: Optional[bytes]


class ExtensionWrapperUriResolver(UriResolver):
    """Defines a resolver that resolves a uri to a wrapper by using an extension wrapper.

    This resolver resolves a uri to a wrapper by using an extension wrapper.\
        The extension wrapper is resolved using the extension wrapper uri resolver.\
        The extension wrapper is then used to resolve the uri to a wrapper.

    Args:
        extension_wrapper_uri (Uri): The uri of the extension wrapper.
    """

    __slots__ = ("extension_wrapper_uri",)

    extension_wrapper_uri: Uri
    """The uri of the extension wrapper."""

    def __init__(self, extension_wrapper_uri: Uri):
        """Initialize a new ExtensionWrapperUriResolver instance."""
        self.extension_wrapper_uri = extension_wrapper_uri

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"ResolverExtension ({self.extension_wrapper_uri})"

    def try_resolve_uri(
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
            uri_package_or_wrapper = self._try_resolve_uri_with_extension(
                uri, client, sub_context
            )

            resolution_context.track_step(
                UriResolutionStep(
                    source_uri=uri,
                    result=uri_package_or_wrapper,
                    description=self.get_step_description(),
                    sub_history=sub_context.get_history(),
                )
            )

            return uri_package_or_wrapper
        except WrapError as err:
            raise UriResolverExtensionError(
                f"Failed to resolve uri: {uri}, using extension resolver: "
                f"({self.extension_wrapper_uri})"
            ) from err
        except InfiniteLoopError as err:
            if err.uri == self.extension_wrapper_uri:
                raise UriResolverExtensionNotFoundError(
                    self.extension_wrapper_uri, sub_context.get_history()
                ) from err
            raise err

    def _try_resolve_uri_with_extension(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a uri or a manifest using the extension wrapper.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for resolving the URI.
            resolution_context (UriResolutionContext): The resolution context.

        Returns:
            MaybeUriOrManifest: The resolved URI or manifest.
        """
        uri_or_manifest: Optional[MaybeUriOrManifest] = client.invoke(
            uri=self.extension_wrapper_uri,
            method="tryResolveUri",
            args={
                "authority": uri.authority,
                "path": uri.path,
            },
            encode_result=False,
            resolution_context=resolution_context,
        )

        if uri_or_manifest is None:
            return uri

        if result_uri := uri_or_manifest.get("uri"):
            return Uri.from_str(result_uri)

        if result_manifest := uri_or_manifest.get("manifest"):
            package = WasmPackage(
                UriResolverExtensionFileReader(self.extension_wrapper_uri, uri, client),
                result_manifest,
            )
            return UriPackage(uri=uri, package=package)

        return uri


__all__ = ["ExtensionWrapperUriResolver", "MaybeUriOrManifest"]
