from polywrap_core import IUriResolver, Uri, Client, IUriResolutionContext, UriPackageOrWrapper, UriResolutionResult

from polywrap_uri_resolvers.builder import build_resolver

from .helpers import UriResolverLike, InfiniteLoopError


class RecursiveResolve(IUriResolver):
    resolver: IUriResolver

    def __init__(self, resolver: UriResolverLike):
        resolver = build_resolver(resolver, None)

    async def try_resolve_uri(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result[UriPackageOrWrapper]:
        if resolution_context.is_resolving(uri):
            return UriResolutionResult.err(
                InfiniteLoopError(uri, resolution_context.get_history())
            )
        
        resolution_context.start_resolving(uri)

        result = await self.resolver.try_resolve_uri(
            uri,
            client,
            resolution_context
        )

        resolution_context.stop_resolving(uri)

        return result
