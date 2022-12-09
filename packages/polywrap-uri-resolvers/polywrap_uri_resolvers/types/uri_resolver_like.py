from __future__ import annotations
from typing import List, Union

from polywrap_core import IUriResolver

from .uri_package import UriPackage
from .uri_redirect import UriRedirect
from .uri_wrapper import UriWrapper
from .static_resolver_like import StaticResolverLike


UriResolverLike = Union[
    StaticResolverLike,
    UriRedirect,
    UriPackage,
    UriWrapper,
    IUriResolver,
    List["UriResolverLike"],
]
