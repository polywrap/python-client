from typing import List, Optional

from polywrap_core import IUriResolver, Uri, IUriResolutionContext, Client
from polywrap_result import Result, Ok

from .uri_resolver_aggregator_base import UriResolverAggregatorBase

class UriResolverAggregator(UriResolverAggregatorBase):
    resolvers: List[IUriResolver]
    name: Optional[str]

    def __init__(self, resolvers: List[IUriResolver]):
      self.resolvers = resolvers

    def get_step_description(self) -> str:
      return self.name or "UriResolverAggregator"

    def get_uri_resolvers(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result[List[IUriResolver]]:
      return Ok(self.resolvers)
