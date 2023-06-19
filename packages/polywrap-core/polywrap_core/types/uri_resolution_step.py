"""This module contains implementation of IUriResolutionStep interface."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .uri import Uri


@dataclass(slots=True, kw_only=True)
class UriResolutionStep:
    """Represents a single step in the resolution of a uri.

    Args:
        source_uri (Uri): The uri that was resolved.
        result (Any): The result of the resolution.
        description (Optional[str]): A description of the resolution step.
        sub_history (Optional[List[UriResolutionStep]]): A list of sub steps\
            that were taken to resolve the uri.
    """

    source_uri: Uri
    result: Any
    description: Optional[str] = None
    sub_history: Optional[List[UriResolutionStep]] = None


__all__ = ["UriResolutionStep"]
