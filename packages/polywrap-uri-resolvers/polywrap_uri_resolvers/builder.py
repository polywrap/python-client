from typing import Optional, List, cast

from .helpers import UriResolverLike
from .aggregator import UriResolverAggregator
from .package_resolver import PackageResolver
from .wrapper_resolver import WrapperResolver

from polywrap_core import IUriResolver, UriPackage, UriWrapper


# TODO: Recheck if this should return result or not
def build_resolver(uri_resolver_like: UriResolverLike, name: Optional[str]) -> IUriResolver:    
    if type(uri_resolver_like) == list:
        resolvers: List[IUriResolver] = list(map(lambda r: build_resolver(cast(UriResolverLike, r), name), uri_resolver_like)) # type: ignore
        return UriResolverAggregator(resolvers)  # type: ignore
    elif isinstance(uri_resolver_like, UriPackage):
        return PackageResolver(uri=uri_resolver_like.uri, wrap_package=uri_resolver_like.package)  # type: ignore
    elif isinstance(uri_resolver_like, UriWrapper):
        return WrapperResolver(uri=uri_resolver_like.uri, wrapper=uri_resolver_like.wrapper)  # type: ignore
    else:
        raise "Unknown resolver-like type" # type: ignore