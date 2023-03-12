"""This module contains the uri resolver interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from polywrap_result import Result

from .invoke import Invoker
from .uri import Uri
from .uri_package_wrapper import UriPackageOrWrapper
from .uri_resolution_context import IUriResolutionContext


@dataclass(slots=True, kw_only=True)
class TryResolveUriOptions:
    """Options for resolving a uri.

    Args:
        no_cache_read: If set to true, the resolveUri function will not \
            use the cache to resolve the uri.
        no_cache_write: If set to true, the resolveUri function will not \
            cache the results
        config: Override the client's config for all resolutions.
        context_id: Id used to track context data set internally.
    """

    uri: Uri
    resolution_context: Optional[IUriResolutionContext] = None


class IUriResolver(ABC):
    """Uri resolver interface."""

    @abstractmethod
    async def try_resolve_uri(
        self, uri: Uri, invoker: Invoker, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        """Try to resolve a uri.

        Args:
            uri: The uri to resolve.
            invoker: The invoker to use for resolving the uri.
            resolution_context: The context for resolving the uri.

        Returns:
            Result[UriPackageOrWrapper]: The resolved uri or an error.
        """
