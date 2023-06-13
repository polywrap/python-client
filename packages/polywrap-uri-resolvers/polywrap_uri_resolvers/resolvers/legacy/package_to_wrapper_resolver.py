"""This module contains the PackageToWrapperResolver class."""
from dataclasses import dataclass
from typing import Optional

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
from polywrap_manifest import DeserializeManifestOptions

from ..abc import ResolverWithHistory


@dataclass(kw_only=True, slots=True)
class PackageToWrapperResolverOptions:
    """Defines the options for the PackageToWrapperResolver.

    Args:
        deserialize_manifest_options (DeserializeManifestOptions): The options\
            to use when deserializing the manifest.
    """

    deserialize_manifest_options: Optional[DeserializeManifestOptions]


class PackageToWrapperResolver(ResolverWithHistory):
    """Defines a resolver that converts packages to wrappers.

    This resolver converts packages to wrappers.\
        If result is an uri, it returns it back.\
        If result is a wrapper, it returns it back.\
        In case of a package, it creates a wrapper and returns it back.
    
    Args:
        resolver (UriResolver): The URI resolver to cache.
        options (PackageToWrapperResolverOptions): The options to use.
    """

    resolver: UriResolver
    options: Optional[PackageToWrapperResolverOptions]

    def __init__(
        self,
        resolver: UriResolver,
        options: Optional[PackageToWrapperResolverOptions] = None,
    ) -> None:
        """Initialize a new PackageToWrapperResolver instance."""
        self.resolver = resolver
        self.options = options
        super().__init__()

    def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve the given URI to a wrapper or a redirected URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use.
            resolution_context (IUriResolutionContext):\
                The resolution context to use.
        
        Returns:
            UriPackageOrWrapper: The resolved URI or wrapper.
        """
        sub_context = resolution_context.create_sub_context()
        result = self.resolver.try_resolve_uri(uri, client, sub_context)
        if isinstance(result, UriPackage):
            wrapper = result.package.create_wrapper()
            result = UriWrapper(uri=uri, wrapper=wrapper)

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=result,
                sub_history=sub_context.get_history(),
                description=self.get_step_description(),
            )
        )
        return result

    def get_step_description(self) -> str:
        """Get the description of the resolution step.

        Returns:
            str: The description of the resolution step.
        """
        return self.__class__.__name__


__all__ = ["PackageToWrapperResolver", "PackageToWrapperResolverOptions"]
