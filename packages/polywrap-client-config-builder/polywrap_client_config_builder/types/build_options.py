"""This module contains the BuildOptions class."""
from dataclasses import dataclass
from typing import Optional

from polywrap_core import UriResolver
from polywrap_uri_resolvers import ResolutionResultCache


@dataclass(slots=True, kw_only=True)
class BuildOptions:
    """BuildOptions defines the options for build method of the client config builder.

    Args:
        resolution_result_cache: The Resolution Result Cache.
        resolver: The URI resolver.
    """

    resolution_result_cache: Optional[ResolutionResultCache] = None
    resolver: Optional[UriResolver] = None


__all__ = ["BuildOptions"]
