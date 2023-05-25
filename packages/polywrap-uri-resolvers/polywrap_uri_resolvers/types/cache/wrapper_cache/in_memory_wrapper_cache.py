"""This module contains the in-memory wrapper cache."""
from typing import Dict, Union

from polywrap_core import Uri, Wrapper

from .wrapper_cache import WrapperCache


class InMemoryWrapperCache(WrapperCache):
    """InMemoryWrapperCache is an in-memory implementation of the wrapper cache interface.

    Attributes:
        map (Dict[Uri, Wrapper]): The map of uris to wrappers.
    """

    map: Dict[Uri, Wrapper]

    def __init__(self):
        """Initialize a new InMemoryWrapperCache instance."""
        self.map = {}

    def get(self, uri: Uri) -> Union[Wrapper, None]:
        """Get a wrapper from the cache by its uri."""
        return self.map.get(uri)

    def set(self, uri: Uri, wrapper: Wrapper) -> None:
        """Set a wrapper in the cache by its uri."""
        self.map[uri] = wrapper
