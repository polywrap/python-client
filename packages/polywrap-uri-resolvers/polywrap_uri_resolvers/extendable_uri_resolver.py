from functools import reduce
from typing import List, cast
from aggregator import UriResolverAggregatorBase
from polywrap_core import Uri, Client, IUriResolutionContext, IUriResolver, UriPackageOrWrapper
from polywrap_result import Result, Err, Ok
from polywrap_uri_resolvers import UriResolverWrapper
class ExtendableUriResolver(UriResolverAggregatorBase):
    name: str

    def __init__(self, name: str):
        self.name = name

    async def get_uri_resolvers(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result[List[IUriResolver]]:
        result = client.get_implementations(uri)

        if result.is_err():
            return cast(Err, result)
    
        def get_wrapper_resolvers(implementation_uri: Uri, resolvers: List[UriResolverWrapper]) -> List[IUriResolver]:
            if not resolution_context.is_resolving(implementation_uri):
                resolver_wrapper = UriResolverWrapper(implementation_uri)
                resolvers.append(resolver_wrapper)
            
            return cast(List[IUriResolver], resolvers)

        return Ok(reduce(get_wrapper_resolvers, result.value)) # type: ignore

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: Client,
        resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        result = await self.get_uri_resolvers(
            uri, client, resolution_context
        )

        if result.is_err():
            return cast(Err, result)

        resolvers: List[IUriResolver] = result.value # type: ignore

        if len(resolvers) == 0:
            return Ok(uri)

        return await self.try_resolve_uri_with_resolvers(
            uri,
            client,
            resolvers,
            resolution_context
        )