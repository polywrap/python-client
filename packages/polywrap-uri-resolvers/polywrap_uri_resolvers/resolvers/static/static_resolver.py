from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    IUriResolutionStep,
    UriPackage,
    UriResolver,
    UriWrapper,
    WrapPackage,
    Uri,
    UriPackageOrWrapper,
    Wrapper,
)

from ...types import StaticResolverLike


class StaticResolver(UriResolver):
    __slots__ = ("uri_map",)

    uri_map: StaticResolverLike

    def __init__(self, uri_map: StaticResolverLike):
        self.uri_map = uri_map

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        result = self.uri_map.get(uri)
        uri_package_or_wrapper: UriPackageOrWrapper = uri
        description: str = "StaticResolver - Miss"

        if result:
            if isinstance(result, WrapPackage):
                description = f"Static - Package ({uri})"
                uri_package_or_wrapper = UriPackage(uri, result)
            elif isinstance(result, Wrapper):
                description = f"Static - Wrapper ({uri})"
                uri_package_or_wrapper = UriWrapper(uri, result)
            else:
                description = f"Static - Redirect ({uri}, {result})"
                uri_package_or_wrapper = result

        step = IUriResolutionStep(
            source_uri=uri, result=uri_package_or_wrapper, description=description
        )
        resolution_context.track_step(step)
        return uri_package_or_wrapper
