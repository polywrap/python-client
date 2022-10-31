from polywrap_core import IUriResolver, UriPackageOrWrapper


class StaticResolver(IUriResolver):
    uri_map: dict[str, UriPackageOrWrapper]

    def __init__(self, static_resolver_like: UriResolverLike):
        pass
