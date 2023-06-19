"""This module contains the uri resolver interface."""
from __future__ import annotations

from typing import Protocol

from .invoker_client import InvokerClient
from .uri import Uri
from .uri_package_wrapper import UriPackageOrWrapper
from .uri_resolution_context import UriResolutionContext


class UriResolver(Protocol):
    """Defines protocol for wrapper uri resolver."""

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a uri.

        Args:
            uri (Uri): The uri to resolve.
            client (InvokerClient): The minimal invoker client \
                to use for resolving the uri.
            resolution_context (UriResolutionContext): The context \
                for resolving the uri.

        Returns:
            UriPackageOrWrapper: result of the URI resolution.
        """
        ...


__all__ = ["UriResolver"]
