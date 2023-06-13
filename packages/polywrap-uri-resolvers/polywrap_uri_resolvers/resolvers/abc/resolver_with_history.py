"""This module contains the ResolverWithHistory abstract class."""
from abc import abstractmethod

from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriResolver,
)


class ResolverWithHistory(UriResolver):
    """Defines an abstract resolver that tracks its steps in\
        the resolution context.

    This is useful for resolvers that doesn't need to manually track \
        their steps in the resolution context.
    """

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI and \
            update the resolution context with the result.

        This method calls the internal abstract method _tryResolveUri before\
        updating the resolution context. Implementations are expect to place\
        resolution logic in _tryResolveUri.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext):\
                The resolution context to update.

        Returns:
            UriPackageOrWrapper: The resolved URI package, wrapper, or URI.
        """
        result = self._try_resolve_uri(uri, client, resolution_context)
        step = UriResolutionStep(
            source_uri=uri, result=result, description=self.get_step_description()
        )
        resolution_context.track_step(step)

        return result

    @abstractmethod
    def get_step_description(self) -> str:
        """Get a description of the resolution step."""

    @abstractmethod
    def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Resolve a URI to a wrap package, a wrapper, or a URI using an internal function.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]):\
                The resolution context to update.
        """


__all__ = ["ResolverWithHistory"]
