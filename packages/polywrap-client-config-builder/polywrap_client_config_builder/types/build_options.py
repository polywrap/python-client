"""This module contains the BuildOptions class."""
from dataclasses import dataclass
from typing import Optional

from polywrap_core import UriResolver
from polywrap_uri_resolvers import WrapperCache


@dataclass(slots=True, kw_only=True)
class BuildOptions:
    """
    Abstract class used to configure the polywrap client before it executes a call.

    The ClientConfig class is created and modified with the ClientConfigBuilder module.
    """

    wrapper_cache: Optional[WrapperCache] = None
    resolver: Optional[UriResolver] = None
