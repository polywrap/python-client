from typing import List, cast
from polywrap_core import IUriResolutionStep, Wrapper, IWrapPackage, UriResolutionResult, IUriResolver, UriPackageOrWrapper, Uri, Client, IUriResolutionContext, UriPackage, UriWrapper
from polywrap_result import Result

from .helpers import UriResolverLike


class StaticResolver(IUriResolver):
    uri_map: dict[str, UriPackageOrWrapper]

    def __init__(self, uri_map: dict[str, UriPackageOrWrapper]):
        self.uri_map = uri_map

    @staticmethod
    def _from(static_resolver_likes: List[UriResolverLike]) -> "StaticResolver":
        uri_map: dict[str, UriPackageOrWrapper] = dict()
        for static_resolver_like in static_resolver_likes:
            if type(static_resolver_like) == list:
                resolver = StaticResolver._from(cast(List[UriResolverLike], static_resolver_like))
                for uri, package_or_wrapper in resolver.uri_map.items():
                    uri_map[uri] = package_or_wrapper

            elif hasattr(static_resolver_like, "uri") and hasattr(static_resolver_like, "package"):
                uri_package = UriPackage(uri=static_resolver_like.uri, package=static_resolver_like.package) # type: ignore
                uri_map[uri_package.uri.uri] = uri_package
            elif hasattr(static_resolver_like, "uri") and hasattr(static_resolver_like, "wrapper"):
                uri_wrapper = UriWrapper(uri=static_resolver_like.uri, wrapper=static_resolver_like.wrapper) # type: ignore
                uri_map[uri_wrapper.uri.uri] = uri_wrapper
            else:
                raise Exception("Unknown static-resolver-like type provided.")

        return StaticResolver(uri_map)

    async def try_resolve_uri(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result["UriPackageOrWrapper"]:
        package_or_wrapper = self.uri_map.get(uri.uri)

        result: Result[UriPackageOrWrapper] = UriResolutionResult.ok(uri)
        description: str = "StaticResolver - Miss"

        if package_or_wrapper:
            if hasattr(package_or_wrapper, "package"):
                result = UriResolutionResult.ok(uri, cast(IWrapPackage, package_or_wrapper))
                description = f"Static - Package ({uri.uri})"
            elif hasattr(package_or_wrapper, "wrapper"):
                result = UriResolutionResult.ok(uri, None, cast(Wrapper, package_or_wrapper))
                description = f"Static - Wrapper ({uri.uri})"

        step = IUriResolutionStep(source_uri=uri, result=result, description=description)
        resolution_context.track_step(step)

        return result
