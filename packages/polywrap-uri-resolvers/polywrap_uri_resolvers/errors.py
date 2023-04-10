"""This module contains all the errors related to URI resolution."""
import json
from dataclasses import asdict
from typing import List, TypeVar

from polywrap_core import IUriResolutionStep, Uri, UriLike

from .utils import get_uri_resolution_path

TUriLike = TypeVar("TUriLike", bound=UriLike)


class UriResolutionError(Exception):
    """Base class for all errors related to URI resolution."""


class InfiniteLoopError(UriResolutionError):
    """Raised when an infinite loop is detected while resolving a URI."""

    def __init__(self, uri: Uri, history: List[IUriResolutionStep[TUriLike]]):
        """Initialize a new InfiniteLoopError instance.

        Args:
            uri (Uri): The URI that caused the infinite loop.
            history (List[IUriResolutionStep[TUriLike]]): The resolution history.
        """
        resolution_path = get_uri_resolution_path(history)
        super().__init__(
            f"An infinite loop was detected while resolving the URI: {uri.uri}\n"
            f"History: {json.dumps([asdict(step) for step in resolution_path], indent=2)}"
        )


class UriResolverExtensionError(UriResolutionError):
    """Base class for all errors related to URI resolver extensions."""


class UriResolverExtensionNotFoundError(UriResolverExtensionError):
    """Raised when an extension resolver wrapper could not be found for a URI."""

    def __init__(self, uri: Uri, history: List[IUriResolutionStep[TUriLike]]):
        """Initialize a new UriResolverExtensionNotFoundError instance.

        Args:
            uri (Uri): The URI that caused the error.
            history (List[IUriResolutionStep[TUriLike]]): The resolution history.
        """
        super().__init__(
            f"Could not find an extension resolver wrapper for the URI: {uri.uri}\n"
            f"History: {json.dumps([asdict(step) for step in history], indent=2)}"
        )
