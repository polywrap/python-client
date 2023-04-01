"""This module contains the interface for a URI resolution context."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from .uri import Uri
from .uri_like import UriLike
from .uri_resolution_step import IUriResolutionStep

TUriLike = TypeVar("TUriLike", bound=UriLike)


class IUriResolutionContext(ABC, Generic[TUriLike]):
    """Defines the interface for a URI resolution context."""

    @abstractmethod
    def is_resolving(self, uri: Uri) -> bool:
        """Check if the given uri is currently being resolved.

        Args:
            uri (Uri): The uri to check.

        Returns:
            bool: True if the uri is currently being resolved, otherwise False.
        """

    @abstractmethod
    def start_resolving(self, uri: Uri) -> None:
        """Start resolving the given uri.

        Args:
            uri (Uri): The uri to start resolving.

        Returns: None
        """

    @abstractmethod
    def stop_resolving(self, uri: Uri) -> None:
        """Stop resolving the given uri.

        Args:
            uri (Uri): The uri to stop resolving.

        Returns: None
        """

    @abstractmethod
    def track_step(self, step: IUriResolutionStep[TUriLike]) -> None:
        """Track the given step in the resolution history.

        Args:
            step (IUriResolutionStep): The step to track.

        Returns: None
        """

    @abstractmethod
    def get_history(self) -> List[IUriResolutionStep[TUriLike]]:
        """Get the resolution history.

        Returns:
            List[IUriResolutionStep]: The resolution history.
        """

    @abstractmethod
    def get_resolution_path(self) -> List[Uri]:
        """Get the resolution path.

        Returns:
            List[Uri]: The ordered list of URI resolution path.
        """

    @abstractmethod
    def create_sub_history_context(self) -> "IUriResolutionContext[TUriLike]":
        """Create a new sub context that shares the same resolution path.

        Returns:
            IUriResolutionContext: The new context.
        """

    @abstractmethod
    def create_sub_context(self) -> "IUriResolutionContext[TUriLike]":
        """Create a new sub context that shares the same resolution history.

        Returns:
            IUriResolutionContext: The new context.
        """
