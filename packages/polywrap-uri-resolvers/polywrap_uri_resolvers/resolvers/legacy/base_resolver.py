"""This module contains the legacy base URI resolver."""
from typing import Dict

from polywrap_core import (
    FileReader,
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolver,
)

from .fs_resolver import FsUriResolver
from .redirect_resolver import RedirectUriResolver


class BaseUriResolver(UriResolver):
    """Defines the base URI resolver.

    Args:
        file_reader (FileReader): The file reader to use.
        redirects (Dict[Uri, Uri]): The redirects to use.
    """

    _fs_resolver: FsUriResolver
    _redirect_resolver: RedirectUriResolver

    def __init__(self, file_reader: FileReader, redirects: Dict[Uri, Uri]):
        """Initialize a new BaseUriResolver instance."""
        self._fs_resolver = FsUriResolver(file_reader)
        self._redirect_resolver = RedirectUriResolver(redirects)

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for resolving the URI.
            resolution_context (UriResolutionContext): The resolution context.

        Returns:
            UriPackageOrWrapper: The resolved URI.
        """
        redirected_uri = self._redirect_resolver.try_resolve_uri(
            uri, client, resolution_context
        )

        return self._fs_resolver.try_resolve_uri(
            redirected_uri, client, resolution_context
        )


__all__ = ["BaseUriResolver"]
