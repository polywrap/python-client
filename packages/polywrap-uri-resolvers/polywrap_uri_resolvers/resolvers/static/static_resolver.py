"""This module contains the StaticResolver class."""
from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriResolver,
    UriWrapper,
)

from ...types import StaticResolverLike


class StaticResolver(UriResolver):
    """Defines the static URI resolver.

    Args:
        uri_map (StaticResolverLike): The URI map to use.
    """

    __slots__ = ("uri_map",)

    uri_map: StaticResolverLike

    def __init__(self, uri_map: StaticResolverLike):
        """Initialize a new StaticResolver instance."""
        self.uri_map = uri_map

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for resolving the URI.
            resolution_context (UriResolutionContext): The resolution context.

        Returns:
            UriPackageOrWrapper: The resolved URI.
        """
        result = self.uri_map.get(uri)

        match result:
            case None:
                description: str = "Static - Miss"
                uri_package_or_wrapper: UriPackageOrWrapper = uri
            case UriPackage():
                description = "Static - Package"
                uri_package_or_wrapper = result
            case UriWrapper():
                description = "Static - Wrapper"
                uri_package_or_wrapper = result
            case _:
                description = f"Static - Redirect ({uri} - {result})"
                uri_package_or_wrapper = result

        step = UriResolutionStep(
            source_uri=uri, result=uri_package_or_wrapper, description=description
        )
        resolution_context.track_step(step)
        return uri_package_or_wrapper


__all__ = ["StaticResolver"]
