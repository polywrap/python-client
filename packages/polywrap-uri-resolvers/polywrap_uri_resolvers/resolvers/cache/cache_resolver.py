from typing import Any, List, Optional, cast

from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    UriPackage,
    UriResolver,
    UriWrapper,
    Uri,
    UriPackageOrWrapper,
    Wrapper,
)
from polywrap_manifest import DeserializeManifestOptions

from ...types import WrapperCache, UriResolutionStep


class CacheResolverOptions:
    deserialize_manifest_options: DeserializeManifestOptions
    end_on_redirect: Optional[bool]


class PackageToWrapperCacheResolver(UriResolver):
    __slots__ = ("name", "resolver_to_cache", "cache", "options")

    name: str
    resolver_to_cache: UriResolver
    cache: WrapperCache
    options: CacheResolverOptions

    def __init__(
        self,
        resolver_to_cache: UriResolver,
        cache: WrapperCache,
        options: CacheResolverOptions,
    ):
        self.resolver_to_cache = resolver_to_cache
        self.cache = cache
        self.options = options

    def get_options(self) -> Any:
        return self.options

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        if wrapper := self.cache.get(uri):
            result = UriWrapper(uri, wrapper)
            resolution_context.track_step(
                UriResolutionStep(
                    source_uri=uri,
                    result=result,
                    description="PackageToWrapperCacheResolver (Cache)",
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

            for uri in resolution_path:
                self.cache.set(uri, uri_wrapper.wrapper)
        elif isinstance(result, UriPackage):
            uri_package = cast(UriPackage[UriPackageOrWrapper], result)
            wrap_package = uri_package.package
            resolution_path = sub_context.get_resolution_path()
            wrapper = await wrap_package.create_wrapper()

            for uri in resolution_path:
                self.cache.set(uri, wrapper)

            result = UriWrapper(uri, wrapper)


        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=result,
                sub_history=sub_context.get_history(),
                description="PackageToWrapperCacheResolver",
            )
        )
        return result
