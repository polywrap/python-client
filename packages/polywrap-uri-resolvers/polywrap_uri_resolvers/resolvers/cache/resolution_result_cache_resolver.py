"""This module contains the ResolutionResultCacheResolver."""

from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriResolver,
)

from ...errors import UriResolutionError
from ...types import ResolutionResultCache


class ResolutionResultCacheResolver(UriResolver):
    """An implementation of IUriResolver that caches the URI resolution result.

    The URI resolution result can be a URI, IWrapPackage, Wrapper, or Error.
    Errors are not cached by default and can be cached by setting the cache_errors option to True.

    Args:
        resolver_to_cache (UriResolver): The URI resolver to cache.
        cache (ResolutionResultCache): The resolution result cache.
        cache_errors (bool): Whether to cache errors.
    """

    __slots__ = ("resolver_to_cache", "cache", "cache_errors")

    resolver_to_cache: UriResolver
    """The URI resolver to cache."""

    cache: ResolutionResultCache
    """The resolution result cache."""

    cache_errors: bool
    """Whether to cache errors."""

    def __init__(
        self,
        resolver_to_cache: UriResolver,
        cache: ResolutionResultCache,
        cache_errors: bool = False,
    ):
        """Initialize a new ResolutionResultCacheResolver instance."""
        self.resolver_to_cache = resolver_to_cache
        self.cache = cache
        self.cache_errors = cache_errors

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the URI with the resolver to cache.\
        If the result is in the cache, it returns the cached result.\
        If the result is not in the cache, it resolves the URI using\
        the inner resolver and caches the result.

        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use.
            resolution_context (UriResolutionContext): The resolution context to use.

        Returns:
            UriPackageOrWrapper: The result of the resolution.
        """
        if cached_result := self.cache.get(uri):
            if isinstance(cached_result, UriResolutionError):
                raise cached_result

            resolution_context.track_step(
                UriResolutionStep(
                    source_uri=uri,
                    result=cached_result,
                    description="ResolutionResultCacheResolver (Cache)",
                )
            )
            return cached_result

        sub_context = resolution_context.create_sub_history_context()
        result: UriPackageOrWrapper

        if self.cache_errors:
            try:
                result = self.resolver_to_cache.try_resolve_uri(
                    uri,
                    client,
                    sub_context,
                )
            except UriResolutionError as error:
                self.cache.set(uri, error)
                raise error
        else:
            result = self.resolver_to_cache.try_resolve_uri(
                uri,
                client,
                sub_context,
            )
            self.cache.set(uri, result)

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=result,
                sub_history=sub_context.get_history(),
                description="ResolutionResultCacheResolver",
            )
        )
        return result


__all__ = ["ResolutionResultCacheResolver"]
