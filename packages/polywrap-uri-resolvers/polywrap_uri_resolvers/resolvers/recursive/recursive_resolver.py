from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    UriResolver,
    Uri,
    UriPackageOrWrapper,
)

from ...errors import InfiniteLoopError


class RecursiveResolver(UriResolver):
    __slots__ = ("resolver",)

    resolver: UriResolver

    def __init__(self, resolver: UriResolver):
        self.resolver = resolver

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        if resolution_context.is_resolving(uri):
            raise InfiniteLoopError(uri, resolution_context.get_history())

        resolution_context.start_resolving(uri)

        uri_package_or_wrapper = await self.resolver.try_resolve_uri(
            uri, client, resolution_context
        )

        if uri_package_or_wrapper != uri:
            uri_package_or_wrapper = await self.try_resolve_uri(
                uri_package_or_wrapper, client, resolution_context
            )

        resolution_context.stop_resolving(uri)

        return uri_package_or_wrapper
