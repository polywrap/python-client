"""This module contains the resolver for wrappers."""
from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    UriWrapper,
    Wrapper,
)

from ..abc import ResolverWithHistory


class WrapperResolver(ResolverWithHistory):
    """Defines the wrapper resolver.

    Attributes:
        uri (Uri): The uri to resolve.
        wrapper (Wrapper[UriPackageOrWrapper]): The wrapper to use.
    """

    __slots__ = ("uri", "wrapper")

    uri: Uri
    wrapper: Wrapper[UriPackageOrWrapper]

    def __init__(self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]):
        """Initialize a new WrapperResolver instance.

        Args:
            uri (Uri): The uri to resolve.
            wrapper (Wrapper[UriPackageOrWrapper]): The wrapper to use.
        """
        self.uri = uri
        self.wrapper = wrapper

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"Wrapper ({self.uri})"

    async def _try_resolve_uri(
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
            UriPackageOrWrapper: The resolved URI, wrap package, or wrapper.
        """
        return uri if uri != self.uri else UriWrapper(uri, self.wrapper)
