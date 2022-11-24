from .abc import IResolverWithHistory
from polywrap_core import Uri, Client, UriPackageOrWrapper, IUriResolutionContext, IWrapPackage, UriResolutionResult
from polywrap_result import Result


class PackageResolver(IResolverWithHistory):
    uri: Uri
    wrap_package: IWrapPackage

    def __init__(self, uri: Uri, wrap_package: IWrapPackage):
        self.uri = uri
        self.wrap_package = wrap_package

    def get_step_description(self) -> str:
        return f'Package ({self.uri.uri})'

    async def _try_resolve_uri(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result["UriPackageOrWrapper"]:
        if uri != self.uri:
            return UriResolutionResult.ok(uri)

        return UriResolutionResult.ok(uri, self.wrap_package)