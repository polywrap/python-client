"""This module contains the RedirectResolver class."""
from polywrap_core import InvokerClient, Uri, UriPackageOrWrapper, UriResolutionContext

from ..abc import ResolverWithHistory


class RedirectResolver(ResolverWithHistory):
    """Defines a resolver that redirects a uri to another uri.

    This resolver redirects a uri to another uri. If the uri to resolve is the same as the\
        uri to redirect from, the uri to redirect to is returned. Otherwise, the uri to resolve\
        is returned.

    Args:
        from_uri (Uri): The uri to redirect from.
        to_uri (Uri): The uri to redirect to.
    """

    __slots__ = ("from_uri", "to_uri")

    from_uri: Uri
    to_uri: Uri

    def __init__(self, from_uri: Uri, to_uri: Uri) -> None:
        """Initialize a new RedirectResolver instance."""
        self.from_uri = from_uri
        self.to_uri = to_uri
        super().__init__()

    def get_step_description(self) -> str:
        """Get the description of the resolver step.

        Returns:
            str: The description of the resolver step.
        """
        return f"Redirect ({self.from_uri} - {self.to_uri})"

    def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the given uri to a wrap package, a wrapper, or a URI.\
            If the given uri is the same as the uri to redirect from, the uri to redirect to is\
            returned. Otherwise, the given uri is returned.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for resolving the URI.
            resolution_context (UriResolutionContext): The resolution context.
        
        Returns:
            UriPackageOrWrapper: The resolved URI package, wrapper, or URI.
        """
        return uri if uri != self.from_uri else self.to_uri


__all__ = ["RedirectResolver"]
