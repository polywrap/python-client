from typing import Optional

from .helpers import UriResolverLike
from .aggregator import UriResolverAggregator

from polywrap_core import IUriResolver

def build_resolver(uri_resolver_like: UriResolverLike, name: Optional[str]) -> IUriResolver:
    if type(uri_resolver_like) == list:
        return UriResolverAggregator(map(lambda r: build_resolver(r, name), uri_resolver_like))