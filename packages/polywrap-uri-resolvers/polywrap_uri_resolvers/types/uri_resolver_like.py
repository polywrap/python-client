"""This module contains the type definition for UriResolverLike.

UriResolverLike is a type that represents a union of types\
    that can be used as a UriResolver.

>>> UriResolverLike = Union[
...     StaticResolverLike,
...     UriPackageOrWrapper,
...     UriRedirect,
...     UriResolver,
...     List[UriResolverLike],
... ]
"""
from __future__ import annotations

from typing import List, Union

from polywrap_core import UriPackageOrWrapper, UriResolver

from .static_resolver_like import StaticResolverLike
from .uri_redirect import UriRedirect

UriResolverLike = Union[
    StaticResolverLike,
    UriPackageOrWrapper,
    UriRedirect,
    UriResolver,
    List["UriResolverLike"],
]
