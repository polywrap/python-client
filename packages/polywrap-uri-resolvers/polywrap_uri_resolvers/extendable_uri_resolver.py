from typing import List, cast
from aggregator import IUriResolverAggregator
from polywrap_core import (
    Uri,
    Client,
    IUriResolutionContext,
    IUriResolver,
    UriPackageOrWrapper,
)
from polywrap_result import Result, Err, Ok
from polywrap_uri_resolvers import UriResolverWrapper


class ExtendableUriResolver(IUriResolverAggregator):
    name: str

    def __init__(self, name: str):
        self.name = name

    async def get_uri_resolvers(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[List[IUriResolver]]:
        result = client.get_implementations(uri)

        if result.is_err():
            return cast(Err, result)

        uri_resolver_impls: List[Uri] = result.unwrap() or []

        resolvers: List[IUriResolver] = [
            UriResolverWrapper(impl)
            for impl in uri_resolver_impls
            if not resolution_context.is_resolving(impl)
        ]

        return Ok(resolvers)

    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        result = await self.get_uri_resolvers(uri, client, resolution_context)

        if result.is_err():
            return cast(Err, result)

        resolvers = result.unwrap()

        return await self.try_resolve_uri_with_resolvers(uri, client, resolvers, resolution_context) if resolvers else Ok(uri)
