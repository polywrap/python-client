"""This module contains implementation of IUriResolutionStep interface."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from polywrap_result import Result

from ..types.uri import Uri
from ..types.uri_package_wrapper import UriPackageOrWrapper
from ..types.uri_resolution_step import IUriResolutionStep


@dataclass(slots=True, kw_only=True)
class UriResolutionStep(IUriResolutionStep):
    """Represents a single step in the resolution of a uri.

    Attributes:
        source_uri: The uri that was resolved.
        result: The result of the resolution.
        description: A description of the resolution step.
        sub_history: A list of sub steps that were taken to resolve the uri.
    """

    source_uri: Uri
    result: Result["UriPackageOrWrapper"]
    description: Optional[str] = None
    sub_history: Optional[List[IUriResolutionStep]] = None
