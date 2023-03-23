"""This module contains the uri resolver interface."""
from __future__ import annotations

from abc import ABC, abstractmethod

from .invoker_client import InvokerClient
from .uri import Uri
from .uri_package_wrapper import UriPackageOrWrapper
from .uri_resolution_context import IUriResolutionContext


class UriResolver(ABC):
    """Defines interface for wrapper uri resolver."""

    @abstractmethod
    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve a uri.

        Args:
            uri: The uri to resolve.
            client: The minimal invoker client to use for resolving the uri.
            resolution_context: The context for resolving the uri.

        Returns:
            UriPackageOrWrapper: result of the URI resolution.
        """
