from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    WrapPackage,
    UriPackage,
    Uri,
    UriPackageOrWrapper,
)

from ..abc import ResolverWithHistory


class PackageResolver(ResolverWithHistory):
    __slots__ = ("uri", "wrap_package")

    uri: Uri
    wrap_package: WrapPackage[UriPackageOrWrapper]

    def __init__(self, uri: Uri, wrap_package: WrapPackage[UriPackageOrWrapper]):
        self.uri = uri
        self.wrap_package = wrap_package

    def get_step_description(self) -> str:
        return f"Package ({self.uri.uri})"

    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        return uri if uri != self.uri else UriPackage(uri, self.wrap_package)
