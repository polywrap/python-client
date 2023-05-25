"""This module contains the wrapper cache interface."""
from abc import abstractmethod
from typing import Protocol, Union

from polywrap_core import Uri, UriPackageOrWrapper
from ....errors import UriResolutionError


class ResolutionResultCache(Protocol):
    """Defines a cache interface for caching resolution results by uri.

    This is used by the resolution result resolver to cache resolution results\
        for a given uri.
    """

    @abstractmethod
    def get(self, uri: Uri) -> Union[UriPackageOrWrapper, UriResolutionError, None]:
        """Get the resolution result from the cache by its uri."""

    @abstractmethod
    def set(self, uri: Uri, result: Union[UriPackageOrWrapper, UriResolutionError]) -> None:
        """Set the resolution result in the cache by its uri."""
