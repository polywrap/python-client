"""This module contains uri resolver handler interface."""
from __future__ import annotations

from abc import ABC, abstractmethod

from polywrap_result import Result

from .uri_package_wrapper import UriPackageOrWrapper
from .uri_resolver import TryResolveUriOptions


class UriResolverHandler(ABC):
    """Uri resolver handler interface."""

    @abstractmethod
    async def try_resolve_uri(
        self, options: TryResolveUriOptions
    ) -> Result[UriPackageOrWrapper]:
        """Try to resolve a uri.

        Args:
            options: The options for resolving the uri.

        Returns:
            Result[UriPackageOrWrapper]: The resolved uri or an error.
        """
