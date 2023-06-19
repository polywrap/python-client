"""This module contains the wrapper cache interface."""
from abc import abstractmethod
from typing import Protocol, Union

from polywrap_core import Uri, UriWrapper


class WrapperCache(Protocol):
    """Defines a cache interface for caching wrappers by uri.

    This is used by the wrapper resolver to cache wrappers for a given uri.
    """

    @abstractmethod
    def get(self, uri: Uri) -> Union[UriWrapper, None]:
        """Get a wrapper from the cache by its uri."""

    @abstractmethod
    def set(self, uri: Uri, wrapper: UriWrapper) -> None:
        """Set a wrapper in the cache by its uri."""


__all__ = ["WrapperCache"]
