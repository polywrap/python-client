from typing import Optional
from helpers import UriResolverLike

from polywrap_core import IUriResolver

def build_resolver(uri_resolver_like: UriResolverLike, name: Optional[str]) -> IUriResolver:
    if type(uri_resolver_like) == list:
        def call_array(uri_resolver: UriResolverLike) -> IUriResolver:
            return build_resolver(uri_resolver, name)

        return UriResolverAggregator(map(call_array, uri_resolver_like))