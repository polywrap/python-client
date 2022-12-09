from typing import Dict

from polywrap_core import (
    Client,
    IFileReader,
    IUriResolutionContext,
    IUriResolver,
    Uri,
    UriPackageOrWrapper,
)
from polywrap_result import Result

from .fs_resolver import FsUriResolver
from .redirect_resolver import RedirectUriResolver


class BaseUriResolver(IUriResolver):
    _fs_resolver: FsUriResolver
    _redirect_resolver: RedirectUriResolver

    def __init__(self, file_reader: IFileReader, redirects: Dict[Uri, Uri]):
        self._fs_resolver = FsUriResolver(file_reader)
        self._redirect_resolver = RedirectUriResolver(redirects)

    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        redirected_uri_result = await self._redirect_resolver.try_resolve_uri(
            uri, client, resolution_context
        )
        if redirected_uri_result.is_err():
            return redirected_uri_result
        redirected_uri = redirected_uri_result.unwrap()

        return await self._fs_resolver.try_resolve_uri(
            redirected_uri, client, resolution_context
        )
