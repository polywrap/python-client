"""This module contains the PackageResolver class."""
from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolutionContext,
    WrapPackage,
)

from ..abc import ResolverWithHistory


class PackageResolver(ResolverWithHistory):
    """Defines a resolver that resolves a uri to a package.

    Args:
        uri (Uri): The uri to resolve.
        package (WrapPackage): The wrap package to return.
    """

    __slots__ = ("uri", "package")

    uri: Uri
    package: WrapPackage

    def __init__(self, uri: Uri, package: WrapPackage):
        """Initialize a new PackageResolver instance."""
        self.uri = uri
        self.package = package
        super().__init__()

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"Package ({self.uri.uri})"

    def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the given uri to a wrap package, a wrapper, or a URI.\
            If the given uri is the same as the uri of the resolver, the wrap package is returned.\
            Otherwise, the given uri is returned.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for\
                resolving the URI.
            resolution_context (UriResolutionContext): The\
                resolution context.
        
        Returns:
            UriPackageOrWrapper: The resolved URI package, wrapper, or URI.
        """
        return uri if uri != self.uri else UriPackage(uri=uri, package=self.package)


__all__ = ["PackageResolver"]
