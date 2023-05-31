"""This module contains the BuilderConfig class."""
from dataclasses import dataclass
from typing import Dict, List, Any

from polywrap_core import (
    Uri,
    UriResolver,
    WrapPackage,
    Wrapper,
)


@dataclass(slots=True, kw_only=True)
class BuilderConfig:
    """BuilderConfig defines the internal configuration for the client config builder.

    Attributes:
        envs (Dict[Uri, Any]): The environment variables for the wrappers.
        interfaces (Dict[Uri, List[Uri]]): The interfaces and their implementations.
        wrappers (Dict[Uri, Wrapper]): The wrappers.
        packages (Dict[Uri, WrapPackage]): The WRAP packages.
        resolvers (List[UriResolver]): The URI resolvers.
        redirects (Dict[Uri, Uri]): The URI redirects.
    """

    envs: Dict[Uri, Any]
    interfaces: Dict[Uri, List[Uri]]
    wrappers: Dict[Uri, Wrapper]
    packages: Dict[Uri, WrapPackage]
    resolvers: List[UriResolver]
    redirects: Dict[Uri, Uri]


__all__ = ["BuilderConfig"]
