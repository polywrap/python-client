from abc import ABC, abstractmethod
from typing import List

from polywrap_core import IUriResolver, Uri, UriResolutionContext
from polywrap_client import PolywrapClient


class UriResolverAggregatorBase(ABC, IUriResolver):
    def __init__(self):
        pass

    @abstractmethod
    def get_uri_resolvers(self, uri: Uri, client: PolywrapClient, resolution_context: UriResolutionContext):
        pass

    def try_resolve_uri(self, uri: Uri, client: PolywrapClient, resolution_context: UriResolutionContext):
        pass

    def try_resolve_uri_with_resolver(self, uri: Uri, client: PolywrapClient, resolvers: List[IUriResolver], resolution_context: UriResolutionContext):
        pass

