"""This module contains uri resolver handler interface."""
from __future__ import annotations

from typing import Any, Optional, Protocol

from .uri import Uri
from .uri_resolution_context import UriResolutionContext


class UriResolverHandler(Protocol):
    """Uri resolver handler protocol."""

    def try_resolve_uri(
        self, uri: Uri, resolution_context: Optional[UriResolutionContext] = None
    ) -> Any:
        """Try to resolve a uri.

        Args:
            uri (Uri): Uri of the wrapper to resolve.
            resolution_context (Optional[IUriResolutionContext]):\
                A URI resolution context

        Returns:
            Any: result of the URI resolution.
        """
        ...


__all__ = ["UriResolverHandler"]
