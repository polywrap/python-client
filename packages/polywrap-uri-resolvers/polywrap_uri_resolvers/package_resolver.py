from .abc.resolver_with_history import IResolverWithHistory
from polywrap_core import Uri, Client, UriPackageOrWrapper, IUriResolutionContext, IWrapPackage, UriResolutionResult
from polywrap_result import Result, Ok


class PackageResolver(IResolverWithHistory):
    __slots__ = ('uri', 'wrap_package')

    uri: Uri
    wrap_package: IWrapPackage

    def __init__(self, uri: Uri, wrap_package: IWrapPackage):
        self.uri = uri
        self.wrap_package = wrap_package

    def get_step_description(self) -> str:
        return f'Package ({self.uri.uri})'

    async def _try_resolve_uri(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result["UriPackageOrWrapper"]:
        return Ok(uri) if uri != self.uri else Ok(self.wrap_package)