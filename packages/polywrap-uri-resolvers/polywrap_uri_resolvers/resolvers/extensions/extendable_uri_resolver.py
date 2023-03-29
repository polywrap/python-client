from typing import List, Optional, cast
from polywrap_core import (
    IUriResolutionContext,
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
)

from ..aggregator import UriResolverAggregator
from .extension_wrapper_uri_resolver import ExtensionWrapperUriResolver


class ExtendableUriResolver(UriResolver):
    DEFAULT_EXT_INTERFACE_URIS = [
        Uri.from_str("wrap://ens/wraps.eth:uri-resolver-ext@1.1.0"),
        Uri.from_str("wrap://ens/wraps.eth:uri-resolver-ext@1.0.0"),
    ]
    resolver_aggregator: UriResolverAggregator

    def __init__(self, resolver_aggregator: UriResolverAggregator):
        self.resolver_aggregator = resolver_aggregator

    @classmethod
    def from_interface(
        cls,
        client: InvokerClient[UriPackageOrWrapper],
        ext_interface_uris: Optional[List[Uri]] = None,
        resolver_name: Optional[str] = None,
    ):
        ext_interface_uris = ext_interface_uris or cls.DEFAULT_EXT_INTERFACE_URIS
        resolver_name = resolver_name or cls.__name__

        uri_resolvers_uris: List[Uri] = []

        for ext_interface_uri in ext_interface_uris:
            uri_resolvers_uris.extend(
                client.get_implementations(ext_interface_uri) or []
            )

        resolvers = [ExtensionWrapperUriResolver(uri) for uri in uri_resolvers_uris]

        return cls(
            UriResolverAggregator(cast(List[UriResolver], resolvers), resolver_name)
        )

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        return await self.resolver_aggregator.try_resolve_uri(
            uri, client, resolution_context
        )