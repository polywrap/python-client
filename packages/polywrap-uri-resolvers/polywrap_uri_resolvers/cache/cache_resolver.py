from typing import Any, List, Optional

from polywrap_core import (
    Client,
    IUriResolutionContext,
    IUriResolutionStep,
    IUriResolver,
    IWrapPackage,
    Uri,
    UriPackageOrWrapper,
    Wrapper,
)
from polywrap_manifest import DeserializeManifestOptions
from polywrap_result import Ok, Result

from .wrapper_cache_interface import IWrapperCache


class CacheResolverOptions:
    deserialize_manifest_options: DeserializeManifestOptions
    end_on_redirect: Optional[bool]


class PackageToWrapperCacheResolver:
    __slots__ = ("name", "resolver_to_cache", "cache", "options")

    name: str
    resolver_to_cache: IUriResolver
    cache: IWrapperCache
    options: CacheResolverOptions

    def __init__(
        self,
        resolver_to_cache: IUriResolver,
        cache: IWrapperCache,
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
        client: Client,
        resolution_context: IUriResolutionContext,
    ) -> Result[UriPackageOrWrapper]:
        if wrapper := self.cache.get(uri):
            result = Ok(wrapper)
            resolution_context.track_step(
                IUriResolutionStep(
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

        if result.is_ok():
            uri_package_or_wrapper = result.unwrap()
            if isinstance(uri_package_or_wrapper, IWrapPackage):
                wrap_package = uri_package_or_wrapper
                resolution_path = sub_context.get_resolution_path()

                wrapper_result = await wrap_package.create_wrapper()

                if wrapper_result.is_err():
                    return wrapper_result

                wrapper = wrapper_result.unwrap()

                for uri in resolution_path:
                    self.cache.set(uri, wrapper)

                result = Ok(wrapper)
            elif isinstance(uri_package_or_wrapper, Wrapper):
                wrapper = uri_package_or_wrapper
                resolution_path: List[Uri] = sub_context.get_resolution_path()

                for uri in resolution_path:
                    self.cache.set(uri, wrapper)

        resolution_context.track_step(
            IUriResolutionStep(
                source_uri=uri,
                result=result,
                sub_history=sub_context.get_history(),
                description="PackageToWrapperCacheResolver",
            )
        )
        return result
