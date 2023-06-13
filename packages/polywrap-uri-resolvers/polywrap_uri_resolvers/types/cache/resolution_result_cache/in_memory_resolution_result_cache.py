"""This module contains the in-memory wrapper cache."""
from typing import Dict, Union

from polywrap_core import Uri, UriPackageOrWrapper

from ....errors import UriResolutionError
from .resolution_result_cache import ResolutionResultCache


class InMemoryResolutionResultCache(ResolutionResultCache):
    """InMemoryResolutionResultCache is an in-memory implementation \
        of the resolution result cache protocol."""

    map: Dict[Uri, Union[UriPackageOrWrapper, UriResolutionError]]
    """The map of uris to resolution result."""

    def __init__(self):
        """Initialize a new InMemoryResolutionResultCache instance."""
        self.map = {}

    def get(self, uri: Uri) -> Union[UriPackageOrWrapper, UriResolutionError, None]:
        """Get the resolution result from the cache by its uri."""
        return self.map.get(uri)

    def set(
        self, uri: Uri, result: Union[UriPackageOrWrapper, UriResolutionError]
    ) -> None:
        """Set the resolution result in the cache by its uri."""
        self.map[uri] = result

    def __str__(self) -> str:
        """Display cache as a string."""
        return f"{self.map}"


__all__ = ["InMemoryResolutionResultCache"]
