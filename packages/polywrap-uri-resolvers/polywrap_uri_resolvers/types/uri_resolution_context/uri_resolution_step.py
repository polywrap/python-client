"""This module contains implementation of IUriResolutionStep interface."""
from __future__ import annotations

from dataclasses import dataclass

from polywrap_core import IUriResolutionStep, UriPackageOrWrapper


@dataclass(slots=True, kw_only=True)
class UriResolutionStep(IUriResolutionStep[UriPackageOrWrapper]):
    """Represents a single step in the resolution of a uri.

    Attributes:
        source_uri: The uri that was resolved.
        result: The result of the resolution.
        description: A description of the resolution step.
        sub_history: A list of sub steps that were taken to resolve the uri.
    """
