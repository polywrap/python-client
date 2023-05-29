"""This module contains the type definition for StaticResolverLike.

StaticResolverLike is a type that represents a union of types\
    that can be used as a StaticResolver.
"""
from typing import Dict

from polywrap_core import Uri, UriPackageOrWrapper

StaticResolverLike = Dict[Uri, UriPackageOrWrapper]
