"""This module contains the UriWrapper type."""
from __future__ import annotations

from typing import Generic, TypeVar

from .uri import Uri
from .uri_like import UriLike
from .wrapper import Wrapper

T = TypeVar("T", bound=UriLike)


class UriWrapper(Generic[T], Uri):
    """UriWrapper is a dataclass that contains a URI and a wrapper.

    Attributes:
        wrapper: The wrapper.
    """

    _wrapper: Wrapper[T]

    def __init__(self, uri: Uri, wrapper: Wrapper[T]) -> None:
        """Initialize a new instance of UriWrapper.

        Args:
            uri: The URI.
            wrapper: The wrapper.
        """
        super().__init__(uri.authority, uri.path)
        self._wrapper = wrapper

    @property
    def wrapper(self) -> Wrapper[T]:
        """Return the wrapper."""
        return self._wrapper
