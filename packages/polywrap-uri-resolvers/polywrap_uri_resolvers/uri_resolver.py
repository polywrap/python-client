from polywrap_core import Uri, IUriResolver, UriPackage, UriWrapper

from .helpers import UriResolverLike


class UriResolver(IUriResolver):
    def __init__(self, resolver_like: UriResolverLike):
        if hasattr(resolver_like, "wrapper") and hasattr(resolver_like, "uri"):
            pass
