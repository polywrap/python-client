"""UriPackageOrWrapper is a Union type alias for a URI, a package, or a wrapper.

UriPackageOrWrapper = Union[Uri, UriWrapper, UriPackage]

Examples:
    >>> from polywrap_core.types import UriPackageOrWrapper
    >>> from polywrap_core.types import Uri
    >>> from polywrap_core.types import UriPackage
    >>> from polywrap_core.types import UriWrapper
    >>> result: UriPackageOrWrapper = Uri("authority", "path")
    >>> match result:
    ...     case Uri() as uri:
    ...         print(uri)
    ...     case _:
    ...         print("Not a URI")
    ...
    wrap://authority/path

"""
from __future__ import annotations

from typing import Union

from .uri import Uri
from .uri_package import UriPackage
from .uri_wrapper import UriWrapper

UriPackageOrWrapper = Union[Uri, UriWrapper, UriPackage]

__all__ = ["UriPackageOrWrapper"]
