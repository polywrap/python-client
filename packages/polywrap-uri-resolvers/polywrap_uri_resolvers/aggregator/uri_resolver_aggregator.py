from typing import List, Optional
from polywrap_core import IUriResolver, Uri, IUriResolutionContext, Client

from .uri_resolver_aggregator_base import UriResolverAggregatorBase

class UriResolverAggregator(UriResolverAggregatorBase):
    resolvers: List[IUriResolver]
    name: Optional[str]

    def __init__(self):
      pass

    def get_step_description(self):
      return self.name or "UriResolverAggregator"

    def get_uri_resolvers(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext):
      pass
