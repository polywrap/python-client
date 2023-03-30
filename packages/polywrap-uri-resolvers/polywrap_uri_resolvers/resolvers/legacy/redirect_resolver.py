"""This module contains the RedirectUriResolver class."""
from typing import Dict

from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
)


class RedirectUriResolver(UriResolver):
    """Defines the redirect URI resolver."""

    _redirects: Dict[Uri, Uri]

    def __init__(self, redirects: Dict[Uri, Uri]):
        """Initialize a new RedirectUriResolver instance.

        Args:
            redirects (Dict[Uri, Uri]): The redirects to use.
        """
        self._redirects = redirects

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> Uri:
        """Try to resolve a URI to redirected URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The resolution context.

        Returns:
            Uri: The resolved URI.
        """
        return self._redirects[uri] if uri in self._redirects else uri
