"""This module contains all the errors related to URI resolution."""
import json
from typing import List

from polywrap_core import Uri, UriResolutionStep, build_clean_uri_history


class UriResolutionError(Exception):
    """Base class for all errors related to URI resolution."""


class InfiniteLoopError(UriResolutionError):
    """Raised when an infinite loop is detected while resolving a URI.

    Args:
        uri (Uri): The URI that caused the infinite loop.
        history (List[UriResolutionStep]): The resolution history.
    """

    uri: Uri
    history: List[UriResolutionStep]

    def __init__(self, uri: Uri, history: List[UriResolutionStep]):
        """Initialize a new InfiniteLoopError instance."""
        self.uri = uri
        self.history = history
        super().__init__(
            f"An infinite loop was detected while resolving the URI: {uri.uri}\n"
            f"History: {json.dumps(build_clean_uri_history(history), indent=2)}"
        )


class UriResolverExtensionError(UriResolutionError):
    """Base class for all errors related to URI resolver extensions."""


class UriResolverExtensionNotFoundError(UriResolverExtensionError):
    """Raised when an extension resolver wrapper could not be found for a URI.

    Args:
        uri (Uri): The URI that caused the error.
        history (List[UriResolutionStep]): The resolution history.
    """

    uri: Uri
    history: List[UriResolutionStep]

    def __init__(self, uri: Uri, history: List[UriResolutionStep]):
        """Initialize a new UriResolverExtensionNotFoundError instance."""
        self.uri = uri
        self.history = history
        super().__init__(
            f"Could not find an extension resolver wrapper for the URI: {uri.uri}\n"
            f"History: {json.dumps(build_clean_uri_history(history), indent=2)}"
        )


__all__ = [
    "UriResolutionError",
    "InfiniteLoopError",
    "UriResolverExtensionError",
    "UriResolverExtensionNotFoundError",
]
