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
from polywrap_result import Ok, Result

from .types import StaticResolverLike


class StaticResolver(IUriResolver):
    __slots__ = ("uri_map",)

    uri_map: StaticResolverLike

    def __init__(self, uri_map: StaticResolverLike):
        self.uri_map = uri_map

    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result["UriPackageOrWrapper"]:
        uri_package_or_wrapper = self.uri_map.get(uri)

        result: Result[UriPackageOrWrapper] = Ok(uri)
        description: str = "StaticResolver - Miss"

        if uri_package_or_wrapper:
            if isinstance(uri_package_or_wrapper, IWrapPackage):
                result = Ok(uri_package_or_wrapper)
                description = f"Static - Package ({uri})"
            elif isinstance(uri_package_or_wrapper, Wrapper):
                result = Ok(uri_package_or_wrapper)
                description = f"Static - Wrapper ({uri})"
            else:
                result = Ok(uri_package_or_wrapper)
                description = f"Static - Redirect ({uri}, {uri_package_or_wrapper})"

        step = IUriResolutionStep(
            source_uri=uri, result=result, description=description
        )
        resolution_context.track_step(step)
        return result
