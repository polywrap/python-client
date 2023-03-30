"""This module contains the PackageResolver class."""
from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    WrapPackage,
)

from ..abc import ResolverWithHistory


class PackageResolver(ResolverWithHistory):
    """Defines a resolver that resolves a uri to a package."""

    __slots__ = ("uri", "wrap_package")

    uri: Uri
    wrap_package: WrapPackage[UriPackageOrWrapper]

    def __init__(self, uri: Uri, wrap_package: WrapPackage[UriPackageOrWrapper]):
        """Initialize a new PackageResolver instance.

        Args:
            uri (Uri): The uri to resolve.
            wrap_package (WrapPackage[UriPackageOrWrapper]): The wrap package to return.
        """
        self.uri = uri
        self.wrap_package = wrap_package

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"Package ({self.uri.uri})"

    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the given uri to a wrap package, a wrapper, or a URI.\
            If the given uri is the same as the uri of the resolver, the wrap package is returned.\
            Otherwise, the given uri is returned.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The\
                resolution context.
        
        Returns:
            UriPackageOrWrapper: The resolved URI package, wrapper, or URI.
        """
        return uri if uri != self.uri else UriPackage(uri, self.wrap_package)
