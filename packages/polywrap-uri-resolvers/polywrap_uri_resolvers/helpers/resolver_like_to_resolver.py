from typing import List, Optional, cast

from polywrap_core import IUriResolver

from ..package_resolver import PackageResolver
from ..redirect_resolver import RedirectResolver
from ..static_resolver import StaticResolver
from ..types import UriPackage, UriRedirect, UriResolverLike, UriWrapper
from ..uri_resolver_aggregator import UriResolverAggregator
from ..wrapper_resolver import WrapperResolver


def resolver_like_to_resolver(
    resolver_like: UriResolverLike, resolver_name: Optional[str] = None
) -> IUriResolver:
    if isinstance(resolver_like, list):
        return UriResolverAggregator(
            [
                resolver_like_to_resolver(x, resolver_name)
                for x in cast(List[UriResolverLike], resolver_like)
            ]
        )
    elif isinstance(resolver_like, dict):
        return StaticResolver(resolver_like)
    elif isinstance(resolver_like, UriRedirect):
        return RedirectResolver(resolver_like.from_uri, resolver_like.to_uri)
    elif isinstance(resolver_like, UriPackage):
        return PackageResolver(resolver_like.uri, resolver_like.package)
    elif isinstance(resolver_like, UriWrapper):
        return WrapperResolver(resolver_like.uri, resolver_like.wrapper)
    else:
        return UriResolverAggregator([resolver_like], resolver_name)
