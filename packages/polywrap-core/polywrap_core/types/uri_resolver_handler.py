"""This module contains uri resolver handler interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .options.uri_resolver_options import TryResolveUriOptions
from .uri_like import UriLike

TUriLike = TypeVar("TUriLike", bound=UriLike)


class UriResolverHandler(ABC, Generic[TUriLike]):
    """Uri resolver handler interface."""

    @abstractmethod
    async def try_resolve_uri(
        self, options: TryResolveUriOptions[TUriLike]
    ) -> TUriLike:
        """Try to resolve a uri.

        Args:
            options: The options for resolving the uri.

        Returns:
            T: result of the URI resolution. Must be a UriLike.
        """
