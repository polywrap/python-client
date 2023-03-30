"""This module contains the wrapper cache interface."""
from abc import ABC, abstractmethod
from typing import Union

from polywrap_core import Uri, UriPackageOrWrapper, Wrapper


class WrapperCache(ABC):
    """Defines a cache interface for caching wrappers by uri.

    This is used by the wrapper resolver to cache wrappers for a given uri.
    """

    @abstractmethod
    def get(self, uri: Uri) -> Union[Wrapper[UriPackageOrWrapper], None]:
        """Get a wrapper from the cache by its uri."""

    @abstractmethod
    def set(self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]) -> None:
        """Set a wrapper in the cache by its uri."""
