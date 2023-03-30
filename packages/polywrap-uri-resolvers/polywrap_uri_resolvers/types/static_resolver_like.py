"""This module contains the type definition for StaticResolverLike.

StaticResolverLike is a type that represents a union of types\
    that can be used as a StaticResolver.

>>> StaticResolverLike = Union[
...     Dict[Uri, Uri],
...     Dict[Uri, WrapPackage],
...     Dict[Uri, Wrapper],
... ]
"""
from typing import Dict, Union

from polywrap_core import Uri, UriPackageOrWrapper, WrapPackage, Wrapper

StaticResolverLike = Union[
    Dict[Uri, Uri],
    Dict[Uri, WrapPackage[UriPackageOrWrapper]],
    Dict[Uri, Wrapper[UriPackageOrWrapper]],
]
