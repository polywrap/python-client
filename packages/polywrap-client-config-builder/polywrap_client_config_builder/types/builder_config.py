"""This module contains the BuilderConfig class."""
from dataclasses import dataclass, field
from typing import Any, Dict, List

from polywrap_core import Uri, UriResolver, WrapPackage, Wrapper


@dataclass(slots=True, kw_only=True)
class BuilderConfig:
    """BuilderConfig defines the internal configuration for the client config builder.

    Args:
        envs (Dict[Uri, Any]): The environment variables for the wrappers.
        interfaces (Dict[Uri, List[Uri]]): The interfaces and their implementations.
        wrappers (Dict[Uri, Wrapper]): The wrappers.
        packages (Dict[Uri, WrapPackage]): The WRAP packages.
        resolvers (List[UriResolver]): The URI resolvers.
        redirects (Dict[Uri, Uri]): The URI redirects.
    """

    envs: Dict[Uri, Any] = field(default_factory=dict)
    interfaces: Dict[Uri, List[Uri]] = field(default_factory=dict)
    wrappers: Dict[Uri, Wrapper] = field(default_factory=dict)
    packages: Dict[Uri, WrapPackage] = field(default_factory=dict)
    resolvers: List[UriResolver] = field(default_factory=list)
    redirects: Dict[Uri, Uri] = field(default_factory=dict)


__all__ = ["BuilderConfig"]
