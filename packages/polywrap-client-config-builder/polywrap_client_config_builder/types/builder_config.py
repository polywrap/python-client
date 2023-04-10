"""This module contains the BuilderConfig class."""
from dataclasses import dataclass
from typing import Dict, List

from polywrap_core import (
    Env,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
    WrapPackage,
    Wrapper,
)


@dataclass(slots=True, kw_only=True)
class BuilderConfig:
    """BuilderConfig defines the internal configuration for the client config builder.

    Attributes:
        envs (Dict[Uri, Env]): The environment variables for the wrappers.
        interfaces (Dict[Uri, List[Uri]]): The interfaces and their implementations.
        wrappers (Dict[Uri, Wrapper[UriPackageOrWrapper]]): The wrappers.
        packages (Dict[Uri, WrapPackage[UriPackageOrWrapper]]): The WRAP packages.
        resolvers (List[UriResolver]): The URI resolvers.
        redirects (Dict[Uri, Uri]): The URI redirects.
    """

    envs: Dict[Uri, Env]
    interfaces: Dict[Uri, List[Uri]]
    wrappers: Dict[Uri, Wrapper[UriPackageOrWrapper]]
    packages: Dict[Uri, WrapPackage[UriPackageOrWrapper]]
    resolvers: List[UriResolver]
    redirects: Dict[Uri, Uri]
