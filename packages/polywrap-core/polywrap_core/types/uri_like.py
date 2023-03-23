"""This module contains the utility for sanitizing and parsing Wrapper URIs."""
from __future__ import annotations

from abc import ABC, abstractmethod
from functools import total_ordering


@total_ordering
class UriLike(ABC):
    """Defines the interface for a URI-like object.

    Examples:
        - Uri
        - UriWrapper
        - UriPackage
    """

    @property
    def scheme(self) -> str:
        """Return the scheme of the URI."""
        return "wrap"

    @property
    @abstractmethod
    def authority(self) -> str:
        """Return the authority of the URI."""

    @property
    @abstractmethod
    def path(self) -> str:
        """Return the path of the URI."""

    @property
    @abstractmethod
    def uri(self) -> str:
        """Return the URI as a string."""

    @staticmethod
    @abstractmethod
    def is_canonical_uri(uri: str) -> bool:
        """Return true if the provided URI is canonical."""

    def __str__(self) -> str:
        """Return the URI as a string."""
        return self.uri

    def __repr__(self) -> str:
        """Return the string URI representation."""
        return f"Uri({self.uri})"

    def __hash__(self) -> int:
        """Return the hash of the URI."""
        return hash(self.uri)

    def __eq__(self, obj: object) -> bool:
        """Return true if the provided object is a Uri and has the same URI."""
        return self.uri == obj.uri if isinstance(obj, UriLike) else False

    def __lt__(self, uri: object) -> bool:
        """Return true if the provided Uri has a URI that is lexicographically\
            less than this Uri."""
        if not isinstance(uri, UriLike):
            raise TypeError(f"Cannot compare Uri to {type(uri)}")
        return self.uri < uri.uri
