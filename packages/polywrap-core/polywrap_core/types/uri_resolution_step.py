"""This module contains the uri resolution step interface."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from .uri import Uri
from .uri_like import UriLike

TUriLike = TypeVar("TUriLike", bound=UriLike)


@dataclass(slots=True, kw_only=True)
class IUriResolutionStep(Generic[TUriLike]):
    """Represents a single step in the resolution of a uri.

    Attributes:
        source_uri (Uri): The uri that was resolved.
        result (T): The result of the resolution. must be a UriLike.
        description: A description of the resolution step.
        sub_history: A list of sub steps that were taken to resolve the uri.
    """

    source_uri: Uri
    result: TUriLike
    description: Optional[str] = None
    sub_history: Optional[List["IUriResolutionStep[TUriLike]"]] = None
