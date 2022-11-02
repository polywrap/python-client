from typing import Optional

from .helpers import UriResolverLike
from .aggregator import UriResolverAggregator
from .package_resolver import PackageResolver
from .wrapper_resolver import WrapperResolver

from polywrap_core import IUriResolver


# TODO: Recheck if this should return result or not
def build_resolver(uri_resolver_like: UriResolverLike, name: Optional[str]) -> IUriResolver:    
    if type(uri_resolver_like) == list:
        return UriResolverAggregator(map(lambda r: build_resolver(r, name), uri_resolver_like)) # type: ignore
    elif hasattr(uri_resolver_like, "uri") and hasattr(uri_resolver_like, "package"):
        return PackageResolver(uri=uri_resolver_like.uri, wrap_package=uri_resolver_like.package) # type: ignore
    elif hasattr(uri_resolver_like, "uri") and hasattr(uri_resolver_like, "wrapper"):
        return WrapperResolver(uri=uri_resolver_like.uri, wrapper=uri_resolver_like.wrapper) # type: ignore
    else:
        raise "Unknown resolver-like type" # type: ignore