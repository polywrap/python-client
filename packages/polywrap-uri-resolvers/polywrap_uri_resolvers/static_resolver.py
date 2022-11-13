from typing import Dict, List, cast
from polywrap_core import IUriResolutionStep, UriResolutionResult, IUriResolver, UriPackageOrWrapper, Uri, Client, IUriResolutionContext, UriPackage, UriWrapper
from polywrap_result import Result, Ok

from .helpers import UriResolverLike


class StaticResolver(IUriResolver):
    uri_map: Dict[Uri, UriPackageOrWrapper]

    def __init__(self, uri_map: Dict[Uri, UriPackageOrWrapper]):
        self.uri_map = uri_map

    @staticmethod
    def from_list(static_resolver_likes: List[UriResolverLike]) -> Result["StaticResolver"]:
        uri_map: Dict[Uri, UriPackageOrWrapper] = {}
        for static_resolver_like in static_resolver_likes:
            if isinstance(static_resolver_like, list):
                resolver = StaticResolver.from_list(cast(List[UriResolverLike], static_resolver_like))
                for uri, package_or_wrapper in resolver.unwrap().uri_map.items():
                    uri_map[uri] = package_or_wrapper
            elif isinstance(static_resolver_like, UriPackage):
                uri_package = UriPackage(uri=static_resolver_like.uri, package=static_resolver_like.package)
                uri_map[uri_package.uri] = uri_package
            elif isinstance(static_resolver_like, UriWrapper):
                uri_wrapper = UriWrapper(uri=static_resolver_like.uri, wrapper=static_resolver_like.wrapper) # type: ignore
                uri_map[uri_wrapper.uri] = uri_wrapper
            else:
                uri_map[static_resolver_like] = static_resolver_like

        return Ok(StaticResolver(uri_map))

    async def try_resolve_uri(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result["UriPackageOrWrapper"]:
        uri_package_or_wrapper = self.uri_map.get(uri)

        result: Result[UriPackageOrWrapper] = UriResolutionResult.ok(uri)
        description: str = "StaticResolver - Miss"

        if uri_package_or_wrapper:
            if isinstance(uri_package_or_wrapper, UriPackage):
                result = UriResolutionResult.ok(uri, uri_package_or_wrapper.package)
                description = f"Static - Package ({uri})"
            elif isinstance(uri_package_or_wrapper, UriWrapper):
                result = UriResolutionResult.ok(uri, None, uri_package_or_wrapper.wrapper)
                description = f"Static - Wrapper ({uri})"
            else:
                result = UriResolutionResult.ok(uri)
                description = f"Static - Wrapper ({uri})"

        step = IUriResolutionStep(source_uri=uri, result=result, description=description)
        resolution_context.track_step(step)
        return result
