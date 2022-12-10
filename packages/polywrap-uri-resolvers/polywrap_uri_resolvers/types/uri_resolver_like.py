from __future__ import annotations

from typing import List, Union

from polywrap_core import IUriResolver

from .static_resolver_like import StaticResolverLike
from .uri_package import UriPackage
from .uri_redirect import UriRedirect
from .uri_wrapper import UriWrapper

UriResolverLike = Union[
    StaticResolverLike,
    UriRedirect,
    UriPackage,
    UriWrapper,
    IUriResolver,
    List["UriResolverLike"],
]
