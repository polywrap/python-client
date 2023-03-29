from __future__ import annotations

from typing import List, Union

from polywrap_core import UriResolver, UriPackageOrWrapper

from .static_resolver_like import StaticResolverLike
from .uri_redirect import UriRedirect

UriResolverLike = Union[
    StaticResolverLike,
    UriPackageOrWrapper,
    UriRedirect,
    UriResolver,
    List["UriResolverLike"],
]
