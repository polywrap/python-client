"""This module contains the in-memory wrapper cache."""
from typing import Dict, Union

from polywrap_core import Uri, UriWrapper

from .wrapper_cache import WrapperCache


class InMemoryWrapperCache(WrapperCache):
    """InMemoryWrapperCache is an in-memory implementation\
        of the wrapper cache interface."""

    map: Dict[Uri, UriWrapper]
    """The map of uris to wrappers."""

    def __init__(self):
        """Initialize a new InMemoryWrapperCache instance."""
        self.map = {}

    def get(self, uri: Uri) -> Union[UriWrapper, None]:
        """Get a wrapper from the cache by its uri."""
        return self.map.get(uri)

    def set(self, uri: Uri, wrapper: UriWrapper) -> None:
        """Set a wrapper in the cache by its uri."""
        self.map[uri] = wrapper


__all__ = ["InMemoryWrapperCache"]
