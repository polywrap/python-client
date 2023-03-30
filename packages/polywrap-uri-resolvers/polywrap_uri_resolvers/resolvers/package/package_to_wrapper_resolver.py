"""This module contains the PackageToWrapperResolver class."""
from dataclasses import dataclass
from typing import Optional, cast

from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolver,
    UriWrapper,
)
from polywrap_manifest import DeserializeManifestOptions

from ...types import UriResolutionStep
from ..abc import ResolverWithHistory


@dataclass(kw_only=True, slots=True)
class PackageToWrapperResolverOptions:
    """Defines the options for the PackageToWrapperResolver.

    Attributes:
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
    
    Attributes:
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
        """Initialize a new PackageToWrapperResolver instance.

        Args:
            resolver (UriResolver): The URI resolver to cache.
            options (PackageToWrapperResolverOptions): The options to use.
        """
        self.resolver = resolver
        self.options = options

    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve the given URI to a wrapper or a redirected URI.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]):\
                The resolution context to use.
        
        Returns:
            UriPackageOrWrapper: The resolved URI or wrapper.
        """
        sub_context = resolution_context.create_sub_context()
        result = await self.resolver.try_resolve_uri(uri, client, sub_context)
        if isinstance(result, UriPackage):
            wrapper = await cast(
                UriPackage[UriPackageOrWrapper], result
            ).package.create_wrapper()
            result = UriWrapper(uri, wrapper)

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
