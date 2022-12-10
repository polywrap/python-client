from polywrap_core import (
    Client,
    IUriResolutionContext,
    IUriResolver,
    Uri,
    UriPackageOrWrapper,
)
from polywrap_result import Err, Result

from .errors import InfiniteLoopError


class RecursiveResolver(IUriResolver):
    __slots__ = ("resolver",)

    resolver: IUriResolver

    def __init__(self, resolver: IUriResolver):
        self.resolver = resolver

    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        if resolution_context.is_resolving(uri):
            return Err(InfiniteLoopError(uri, resolution_context.get_history()))

        resolution_context.start_resolving(uri)

        result = await self.resolver.try_resolve_uri(uri, client, resolution_context)

        if result.is_ok():
            uri_package_or_wrapper = result.unwrap()
            if (
                isinstance(uri_package_or_wrapper, Uri)
                and uri_package_or_wrapper != uri
            ):
                result = await self.try_resolve_uri(
                    uri_package_or_wrapper, client, resolution_context
                )

        resolution_context.stop_resolving(uri)

        return result
