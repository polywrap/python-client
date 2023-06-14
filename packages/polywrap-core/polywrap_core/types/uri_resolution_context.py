"""This module contains implementation of IUriResolutionContext interface."""
from typing import List, Optional, Set

from .uri import Uri
from .uri_resolution_step import UriResolutionStep


class UriResolutionContext:
    """Represents the context of a uri resolution.

    Args:
        resolving_uri_set (Set[Uri]): A set of uris that\
            are currently being resolved.
        resolution_path (List[Uri]): A list of uris in the order that\
            they are being resolved.
        history (List[UriResolutionStep]): A list of steps \
            that have been taken to resolve the uri.
    """

    resolving_uri_set: Set[Uri]
    """A set of uris that are currently being resolved."""

    resolution_path: List[Uri]
    """A list of uris in the order that they are being resolved."""

    history: List[UriResolutionStep]
    """A list of steps that have been taken to resolve the uri."""

    __slots__ = ("resolving_uri_set", "resolution_path", "history")

    def __init__(
        self,
        resolving_uri_set: Optional[Set[Uri]] = None,
        resolution_path: Optional[List[Uri]] = None,
        history: Optional[List[UriResolutionStep]] = None,
    ):
        """Initialize a new instance of UriResolutionContext."""
        self.resolving_uri_set = resolving_uri_set or set()
        self.resolution_path = resolution_path or []
        self.history = history or []

    def is_resolving(self, uri: Uri) -> bool:
        """Check if the given uri is currently being resolved.

        Args:
            uri (Uri): The uri to check.

        Returns:
            bool: True if the uri is currently being resolved, otherwise False.
        """
        return uri in self.resolving_uri_set

    def start_resolving(self, uri: Uri) -> None:
        """Start resolving the given uri.

        Args:
            uri (Uri): The uri to start resolving.

        Returns: None
        """
        self.resolving_uri_set.add(uri)
        self.resolution_path.append(uri)

    def stop_resolving(self, uri: Uri) -> None:
        """Stop resolving the given uri.

        Args:
            uri (Uri): The uri to stop resolving.

        Returns: None
        """
        self.resolving_uri_set.remove(uri)

    def track_step(self, step: UriResolutionStep) -> None:
        """Track the given step in the resolution history.

        Args:
            step (UriResolutionStep): The step to track.

        Returns: None
        """
        self.history.append(step)

    def get_history(self) -> List[UriResolutionStep]:
        """Get the resolution history.

        Returns:
            List[UriResolutionStep]: The resolution history.
        """
        return self.history

    def get_resolution_path(self) -> List[Uri]:
        """Get the resolution path.

        Returns:
            List[Uri]: The ordered list of URI resolution path.
        """
        return self.resolution_path

    def create_sub_history_context(self) -> "UriResolutionContext":
        """Create a new sub context that shares the same resolution path.

        Returns:
            UriResolutionContext: The new context.
        """
        return UriResolutionContext(
            resolving_uri_set=self.resolving_uri_set,
            resolution_path=self.resolution_path,
        )

    def create_sub_context(self) -> "UriResolutionContext":
        """Create a new sub context that shares the same resolution history.

        Returns:
            UriResolutionContext: The new context.
        """
        return UriResolutionContext(
            resolving_uri_set=self.resolving_uri_set, history=self.history
        )


__all__ = ["UriResolutionContext"]
