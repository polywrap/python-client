"""This module contains the ExtendableUriResolver class."""
from typing import List, Optional

from polywrap_core import InvokerClient, Uri, UriResolutionContext, UriResolver

from ..aggregator import UriResolverAggregatorBase
from .extension_wrapper_uri_resolver import ExtensionWrapperUriResolver


class ExtendableUriResolver(UriResolverAggregatorBase):
    """Defines a resolver that resolves a uri to a wrapper by using extension wrappers.

    This resolver resolves a uri to a wrapper by using extension wrappers.\
        The extension wrappers are resolved using the extension wrapper uri resolver.\
        The extension wrappers are aggregated using the uri resolver aggregator.\
        The aggregated extension wrapper resolver is then used to resolve\
        the uri to a wrapper.

    Args:
        ext_interface_uris (Optional[List[Uri]]): The list of extension\
            interface uris. Defaults to the default list of extension\
            interface uris.
        resolver_name (Optional[str]): The name of the resolver. Defaults\
            to the class name.
    """

    DEFAULT_EXT_INTERFACE_URIS = [
        Uri.from_str("wrap://ens/wraps.eth:uri-resolver-ext@1.1.0"),
        Uri.from_str("wrap://ens/wraps.eth:uri-resolver-ext@1.0.0"),
    ]
    """The default list of extension interface uris."""

    ext_interface_uris: List[Uri]
    """The list of extension interface uris."""

    resolver_name: str
    """The name of the resolver."""

    def __init__(
        self,
        ext_interface_uris: Optional[List[Uri]] = None,
        resolver_name: Optional[str] = None,
    ):
        """Initialize a new ExtendableUriResolver instance."""
        self.ext_interface_uris = ext_interface_uris or self.DEFAULT_EXT_INTERFACE_URIS
        self.resolver_name = resolver_name or self.__class__.__name__
        super().__init__()

    def get_step_description(self) -> Optional[str]:
        """Get the description of the resolution step."""
        return self.resolver_name

    def get_resolvers(
        self, client: InvokerClient, resolution_context: UriResolutionContext
    ) -> List[UriResolver]:
        """Get the list of resolvers to aggregate."""
        uri_resolvers_uris: List[Uri] = []

        for ext_interface_uri in self.ext_interface_uris:
            uri_resolvers_uris.extend(
                client.get_implementations(ext_interface_uri, apply_resolution=False)
                or []
            )

        return [
            ExtensionWrapperUriResolver(uri)
            for uri in uri_resolvers_uris
            if not resolution_context.is_resolving(uri)
        ]


__all__ = ["ExtendableUriResolver"]
