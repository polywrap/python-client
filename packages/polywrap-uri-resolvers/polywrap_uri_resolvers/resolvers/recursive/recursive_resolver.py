"""This module contains the recursive resolver."""
from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
)

from ...errors import InfiniteLoopError


class RecursiveResolver(UriResolver):
    """Defines the recursive resolver.

    The recursive resolver is a wrapper around another resolver that\
    recursively resolves the URI until the result is no longer a URI.

    Args:
        resolver (UriResolver): The resolver to use.
    """

    __slots__ = ("resolver",)

    resolver: UriResolver

    def __init__(self, resolver: UriResolver):
        """Initialize a new RecursiveResolver instance.

        Args:
            resolver (UriResolver): The resolver to use.
        """
        self.resolver = resolver

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The resolution context.

        Returns:
            UriPackageOrWrapper: The resolved URI.
        """
        if resolution_context.is_resolving(uri):
            raise InfiniteLoopError(uri, resolution_context.get_history())

        resolution_context.start_resolving(uri)

        uri_package_or_wrapper = await self.resolver.try_resolve_uri(
            uri, client, resolution_context
        )

        if uri_package_or_wrapper != uri:
            uri_package_or_wrapper = await self.try_resolve_uri(
                uri_package_or_wrapper, client, resolution_context
            )

        resolution_context.stop_resolving(uri)

        return uri_package_or_wrapper
