"""This module contains the resolver for wrappers."""
from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriWrapper,
    Wrapper,
)

from ..abc import ResolverWithHistory


class WrapperResolver(ResolverWithHistory):
    """Defines the wrapper resolver.

    Args:
        uri (Uri): The uri to resolve.
        wrapper (Wrapper): The wrapper to use.
    """

    __slots__ = ("uri", "wrapper")

    uri: Uri
    wrapper: Wrapper

    def __init__(self, uri: Uri, wrapper: Wrapper):
        """Initialize a new WrapperResolver instance."""
        self.uri = uri
        self.wrapper = wrapper
        super().__init__()

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"Wrapper ({self.uri})"

    def _try_resolve_uri(
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
            UriPackageOrWrapper: The resolved URI, wrap package, or wrapper.
        """
        return uri if uri != self.uri else UriWrapper(uri=uri, wrapper=self.wrapper)


__all__ = ["WrapperResolver"]
