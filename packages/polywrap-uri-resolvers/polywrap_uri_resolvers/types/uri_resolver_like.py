from __future__ import annotations

from typing import List, Union

from polywrap_core import IUriResolver

from .static_resolver_like import StaticResolverLike
from .uri_redirect import UriRedirect

UriResolverLike = Union[
    StaticResolverLike,
    UriRedirect,
    IUriResolver,
    List["UriResolverLike"],
]
