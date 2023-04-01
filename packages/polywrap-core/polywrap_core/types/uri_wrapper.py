"""This module contains the UriWrapper type."""
from __future__ import annotations

from typing import Generic, TypeVar

from .uri import Uri
from .uri_like import UriLike
from .wrapper import Wrapper

TUriLike = TypeVar("TUriLike", bound=UriLike)


class UriWrapper(Generic[TUriLike], Uri):
    """UriWrapper is a dataclass that contains a URI and a wrapper.

    Attributes:
        wrapper: The wrapper.
    """

    _wrapper: Wrapper[TUriLike]

    def __init__(self, uri: Uri, wrapper: Wrapper[TUriLike]) -> None:
        """Initialize a new instance of UriWrapper.

        Args:
            uri: The URI.
            wrapper: The wrapper.
        """
        super().__init__(uri.authority, uri.path)
        self._wrapper = wrapper

    @property
    def wrapper(self) -> Wrapper[TUriLike]:
        """Return the wrapper."""
        return self._wrapper
