"""This module contains the RedirectUriResolver class."""
from typing import Dict

from polywrap_core import InvokerClient, Uri, UriResolutionContext, UriResolver


class RedirectUriResolver(UriResolver):
    """Defines the redirect URI resolver.

    Args:
        redirects (Dict[Uri, Uri]): The redirects to use.
    """

    _redirects: Dict[Uri, Uri]

    def __init__(self, redirects: Dict[Uri, Uri]):
        """Initialize a new RedirectUriResolver instance."""
        self._redirects = redirects

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> Uri:
        """Try to resolve a URI to redirected URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for resolving the URI.
            resolution_context (UriResolutionContext): The resolution context.

        Returns:
            Uri: The resolved URI.
        """
        return self._redirects[uri] if uri in self._redirects else uri


__all__ = ["RedirectUriResolver"]
