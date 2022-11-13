from typing import Optional, List, cast

from .helpers import UriResolverLike
from .aggregator import UriResolverAggregator
from .package_resolver import PackageResolver
from .wrapper_resolver import WrapperResolver

from polywrap_core import IUriResolver, UriPackage, UriWrapper


# TODO: Recheck if this should return result or not
def build_resolver(
    uri_resolver_like: UriResolverLike, name: Optional[str]
) -> IUriResolver:
    if isinstance(uri_resolver_like, list):
        resolvers: List[IUriResolver] = list(
            map(
                lambda r: build_resolver(r, name),
                uri_resolver_like,
            )
        )
        return UriResolverAggregator(resolvers)
    elif isinstance(uri_resolver_like, UriPackage):
        return PackageResolver(
            uri=uri_resolver_like.uri, wrap_package=uri_resolver_like.package
        )
    elif isinstance(uri_resolver_like, UriWrapper):
        return WrapperResolver(
            uri=uri_resolver_like.uri, wrapper=uri_resolver_like.wrapper
        )
    else:
        raise ValueError("Unknown resolver-like value")
