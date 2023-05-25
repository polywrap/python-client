"""This module contains the in-memory wrapper cache."""
from typing import Dict, Union

from polywrap_core import Uri, UriPackageOrWrapper

from .resolution_result_cache import ResolutionResultCache
from ....errors import UriResolutionError


class InMemoryResolutionResultCache(ResolutionResultCache):
    """InMemoryResolutionResultCache is an in-memory implementation \
        of the resolution result cache interface.

    Attributes:
        map (Dict[Uri, Union[UriPackageOrWrapper, UriResolutionError]]): The map of uris to resolution result.
    """

    map: Dict[Uri, Union[UriPackageOrWrapper, UriResolutionError]]

    def __init__(self):
        """Initialize a new InMemoryResolutionResultCache instance."""
        self.map = {}

    def get(self, uri: Uri) -> Union[UriPackageOrWrapper, UriResolutionError, None]:
        """Get the resolution result from the cache by its uri."""
        return self.map.get(uri)

    def set(self, uri: Uri, result: Union[UriPackageOrWrapper, UriResolutionError]) -> None:
        """Set the resolution result in the cache by its uri."""
        self.map[uri] = result
