"""This module contains all the errors related to URI resolution."""
from polywrap_core import Uri


class UriResolutionError(Exception):
    """Base class for all errors related to URI resolution."""


class InfiniteLoopError(UriResolutionError):
    """Raised when an infinite loop is detected while resolving a URI.

    Args:
        uri (Uri): The URI that caused the infinite loop.
    """

    uri: Uri

    def __init__(self, uri: Uri):
        """Initialize a new InfiniteLoopError instance."""
        self.uri = uri
        super().__init__(
            f"An infinite loop was detected while resolving the URI: {uri.uri}\n"
        )


class UriResolverExtensionError(UriResolutionError):
    """Base class for all errors related to URI resolver extensions."""


class UriResolverExtensionNotFoundError(UriResolverExtensionError):
    """Raised when an extension resolver wrapper could not be found for a URI.

    Args:
        uri (Uri): The URI that caused the error.
    """

    uri: Uri

    def __init__(self, uri: Uri):
        """Initialize a new UriResolverExtensionNotFoundError instance."""
        self.uri = uri
        super().__init__(
            f"Could not find an extension resolver wrapper for the URI: {uri.uri}\n"
        )


__all__ = [
    "UriResolutionError",
    "InfiniteLoopError",
    "UriResolverExtensionError",
    "UriResolverExtensionNotFoundError",
]
