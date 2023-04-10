"""This module contains the WrapperCacheResolver."""
from dataclasses import dataclass
from typing import List, Optional, Union, cast

from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
    UriWrapper,
    Wrapper,
)
from polywrap_manifest import DeserializeManifestOptions

from ...types import UriResolutionStep, WrapperCache


@dataclass(kw_only=True, slots=True)
class WrapperCacheResolverOptions:
    """Defines the options for the WrapperCacheResolver.

    Attributes:
        deserialize_manifest_options (DeserializeManifestOptions): The options\
            to use when deserializing the manifest.
        end_on_redirect (Optional[bool]): Whether to end the resolution\
            process when a redirect is encountered. Defaults to False.
    """

    deserialize_manifest_options: DeserializeManifestOptions
    end_on_redirect: Optional[bool]


class WrapperCacheResolver(UriResolver):
    """Defines a resolver that caches wrappers by uri.

    This resolver caches the results of URI Resolution.\
        If result is an uri or package, it returns it back without caching.\
        If result is a wrapper, it caches the wrapper and returns it back.

    Attributes:
        resolver_to_cache (UriResolver): The URI resolver to cache.
        cache (WrapperCache): The cache to use.
        options (CacheResolverOptions): The options to use.
    """

    __slots__ = ("resolver_to_cache", "cache", "options")

    resolver_to_cache: UriResolver
    cache: WrapperCache
    options: Optional[WrapperCacheResolverOptions]

    def __init__(
        self,
        resolver_to_cache: UriResolver,
        cache: WrapperCache,
        options: Optional[WrapperCacheResolverOptions] = None,
    ):
        """Initialize a new PackageToWrapperCacheResolver instance.

        Args:
            resolver_to_cache (UriResolver): The URI resolver to cache.
            cache (WrapperCache): The cache to use.
            options (CacheResolverOptions): The options to use.
        """
        self.resolver_to_cache = resolver_to_cache
        self.cache = cache
        self.options = options

    def get_options(self) -> Union[WrapperCacheResolverOptions, None]:
        """Get the options of the resolver.

        Returns:
            CacheResolverOptions: The options of the resolver.
        """
        return self.options

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrapper, or a URI.

        This method tries to resolve the uri with the resolver to cache.\
            If the result is an uri or package, it returns it back without caching.\
            If the result is a wrapper, it caches the wrapper and returns it back.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use.
            resolution_context (IUriResolutionContext): The resolution\
                context to use.
        
        Returns:
            UriPackageOrWrapper: The result of the resolution.
        """
        if wrapper := self.cache.get(uri):
            result = UriWrapper(uri, wrapper)
            resolution_context.track_step(
                UriResolutionStep(
                    source_uri=uri,
                    result=result,
                    description="WrapperCacheResolver (Cache Hit)",
                )
            )
            return result

        sub_context = resolution_context.create_sub_history_context()

        result = await self.resolver_to_cache.try_resolve_uri(
            uri,
            client,
            sub_context,
        )

        if isinstance(result, Wrapper):
            uri_wrapper = cast(UriWrapper[UriPackageOrWrapper], result)
            resolution_path: List[Uri] = sub_context.get_resolution_path()

            for cache_uri in resolution_path:
                self.cache.set(cache_uri, uri_wrapper.wrapper)

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=result,
                sub_history=sub_context.get_history(),
                description="WrapperCacheResolver (Cache Miss)",
            )
        )
        return result
