"""This module contains the in-memory wrapper cache."""
from typing import Dict, Union

from polywrap_core import Uri, Wrapper, UriPackageOrWrapper

from .resolution_result_cache import ResolutionResultCache


class InMemoryResolutionResultCache(ResolutionResultCache):
    """InMemoryResolutionResultCache is an in-memory implementation \
        of the resolution result cache interface.

    Attributes:
        map (Dict[Uri, UriPackageOrWrapper]): The map of uris to resolution result.
    """

    map: Dict[Uri, UriPackageOrWrapper]

    def __init__(self):
        """Initialize a new InMemoryResolutionResultCache instance."""
        self.map = {}

    def get(self, uri: Uri) -> Union[UriPackageOrWrapper, None]:
        """Get a resolution result from the cache by its uri."""
        return self.map.get(uri)

    def set(self, uri: Uri, result: UriPackageOrWrapper) -> None:
        """Set a resolution result in the cache by its uri."""
        self.map[uri] = result
