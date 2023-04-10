"""This module contains the BuildOptions class."""
from dataclasses import dataclass
from typing import Optional

from polywrap_core import UriResolver
from polywrap_uri_resolvers import WrapperCache


@dataclass(slots=True, kw_only=True)
class BuildOptions:
    """BuildOptions defines the options for build method of the client config builder.

    Attributes:
        wrapper_cache: The wrapper cache.
        resolver: The URI resolver.
    """

    wrapper_cache: Optional[WrapperCache] = None
    resolver: Optional[UriResolver] = None
