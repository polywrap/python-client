"""This module contains the TryResolveUriOptions type."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from ..uri import Uri
from ..uri_like import UriLike
from ..uri_resolution_context import IUriResolutionContext

TUriLike = TypeVar("TUriLike", bound=UriLike)


@dataclass(slots=True, kw_only=True)
class TryResolveUriOptions(Generic[TUriLike]):
    """Options for resolving a uri.

    Args:
        uri (Uri): Uri of the wrapper to resolve.
        resolution_context (Optional[IUriResolutionContext]): A URI resolution context
    """

    uri: Uri
    resolution_context: Optional[IUriResolutionContext[TUriLike]] = None
