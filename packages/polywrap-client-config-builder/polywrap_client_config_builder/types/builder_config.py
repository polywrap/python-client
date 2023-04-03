"""This module contains the BuilderConfig class."""
from dataclasses import dataclass
from typing import Any, Dict, List

from polywrap_core import Uri, UriPackageOrWrapper, UriResolver, WrapPackage, Wrapper


@dataclass(slots=True, kw_only=True)
class BuilderConfig:
    """
    Abstract class used to configure the polywrap client before it executes a call.

    The ClientConfig class is created and modified with the ClientConfigBuilder module.
    """

    envs: Dict[Uri, Dict[str, Any]]
    interfaces: Dict[Uri, List[Uri]]
    wrappers: Dict[Uri, Wrapper[UriPackageOrWrapper]]
    packages: Dict[Uri, WrapPackage[UriPackageOrWrapper]]
    resolvers: List[UriResolver]
    redirects: Dict[Uri, Uri]
