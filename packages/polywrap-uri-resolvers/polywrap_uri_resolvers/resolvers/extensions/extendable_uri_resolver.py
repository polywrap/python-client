"""This module contains the ExtendableUriResolver class."""
from typing import List, Optional, cast

from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
)

from ..aggregator import UriResolverAggregator
from .extension_wrapper_uri_resolver import ExtensionWrapperUriResolver


class ExtendableUriResolver(UriResolver):
    """Defines a resolver that resolves a uri to a wrapper by using extension wrappers.

    This resolver resolves a uri to a wrapper by using extension wrappers.\
        The extension wrappers are resolved using the extension wrapper uri resolver.\
        The extension wrappers are aggregated using the uri resolver aggregator.\
        The aggregated extension wrapper resolver is then used to resolve\
        the uri to a wrapper.

    Attributes:
        DEFAULT_EXT_INTERFACE_URIS (List[Uri]): The default list of extension\
            interface uris.
        resolver_aggregator (UriResolverAggregator): The resolver aggregator\
            to use for resolving the extension interface uris.
    """

    DEFAULT_EXT_INTERFACE_URIS = [
        Uri.from_str("wrap://ens/wraps.eth:uri-resolver-ext@1.1.0"),
        Uri.from_str("wrap://ens/wraps.eth:uri-resolver-ext@1.0.0"),
    ]
    resolver_aggregator: UriResolverAggregator

    def __init__(self, resolver_aggregator: UriResolverAggregator):
        """Initialize a new ExtendableUriResolver instance.
        
        Args:
            resolver_aggregator (UriResolverAggregator): The resolver aggregator\
                to use for resolving the extension interface uris.
        """
        self.resolver_aggregator = resolver_aggregator

    @classmethod
    def from_interface(
        cls,
        client: InvokerClient[UriPackageOrWrapper],
        ext_interface_uris: Optional[List[Uri]] = None,
        resolver_name: Optional[str] = None,
    ):
        """Create a new ExtendableUriResolver instance from a list of extension interface uris.

        Args:
            client (InvokerClient[UriPackageOrWrapper]): The client to use for\
                resolving the extension interface uris.
            ext_interface_uris (Optional[List[Uri]]): The list of extension\
                interface uris. Defaults to the default list of extension\
                interface uris.
            resolver_name (Optional[str]): The name of the resolver. Defaults\
                to the class name.

        Returns:
            ExtendableUriResolver: The new ExtendableUriResolver instance.
        """
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
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]): The\
                resolution context.
        
        Returns:
            UriPackageOrWrapper: The resolved URI, wrap package, or wrapper.
        """
        return await self.resolver_aggregator.try_resolve_uri(
            uri, client, resolution_context
        )
