from polywrap_core import IUriResolver, IUriResolverLike


class RecursiveResolve(IUriResolver):
    resolver: IUriResolver

    def __init__(self, resolver: IUriResolverLike):
        pass
