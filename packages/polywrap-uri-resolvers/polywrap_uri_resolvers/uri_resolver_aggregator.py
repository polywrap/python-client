from typing import List, Optional

from polywrap_core import Client, IUriResolutionContext, IUriResolver, Uri
from polywrap_result import Ok, Result

from .abc.uri_resolver_aggregator import IUriResolverAggregator


class UriResolverAggregator(IUriResolverAggregator):
    __slots__ = ("resolvers", "name")

    resolvers: List[IUriResolver]
    name: Optional[str]

    def __init__(self, resolvers: List[IUriResolver], name: Optional[str] = None):
        self.name = name
        self.resolvers = resolvers

    def get_step_description(self) -> str:
        return self.name or "UriResolverAggregator"

    async def get_uri_resolvers(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[List[IUriResolver]]:
        return Ok(self.resolvers)
