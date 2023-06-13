"""This module contains the WrapperCacheResolver."""
from dataclasses import dataclass
from typing import List, Optional, Union

from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriResolver,
    UriWrapper,
)
from polywrap_manifest import DeserializeManifestOptions

from .wrapper_cache import WrapperCache


@dataclass(kw_only=True, slots=True)
class WrapperCacheResolverOptions:
    """Defines the options for the WrapperCacheResolver.

    Args:
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

    Args:
        resolver_to_cache (UriResolver): The URI resolver to cache.
        cache (WrapperCache): The cache to use.
        options (Optional[WrapperCacheResolverOptions]): The options to use.
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
        """Initialize a new PackageToWrapperCacheResolver instance."""
        self.resolver_to_cache = resolver_to_cache
        self.cache = cache
        self.options = options

    def get_options(self) -> Union[WrapperCacheResolverOptions, None]:
        """Get the options of the resolver.

        Returns:
            CacheResolverOptions: The options of the resolver.
        """
        return self.options

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrapper, or a URI.

        This method tries to resolve the uri with the resolver to cache.\
            If the result is an uri or package, it returns it back without caching.\
            If the result is a wrapper, it caches the wrapper and returns it back.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use.
            resolution_context (UriResolutionContext): The resolution\
                context to use.
        
        Returns:
            UriPackageOrWrapper: The result of the resolution.
        """
        if uri_wrapper := self.cache.get(uri):
            resolution_context.track_step(
                UriResolutionStep(
                    source_uri=uri,
                    result=uri_wrapper,
                    description="WrapperCacheResolver (Cache Hit)",
                )
            )
            return uri_wrapper

        sub_context = resolution_context.create_sub_history_context()

        result = self.resolver_to_cache.try_resolve_uri(
            uri,
            client,
            sub_context,
        )

        if isinstance(result, UriWrapper):
            resolution_path: List[Uri] = sub_context.get_resolution_path()

            for cache_uri in resolution_path:
                self.cache.set(cache_uri, result)

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=result,
                sub_history=sub_context.get_history(),
                description="WrapperCacheResolver (Cache Miss)",
            )
        )
        return result


__all__ = ["WrapperCacheResolver", "WrapperCacheResolverOptions"]
