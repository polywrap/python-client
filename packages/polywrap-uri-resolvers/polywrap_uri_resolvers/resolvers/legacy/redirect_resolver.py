from typing import Dict

from polywrap_core import InvokerClient, IUriResolutionContext, UriResolver, Uri, UriPackageOrWrapper


class RedirectUriResolver(UriResolver):
    _redirects: Dict[Uri, Uri]

    def __init__(self, redirects: Dict[Uri, Uri]):
        self._redirects = redirects

    async def try_resolve_uri(
        self, uri: Uri, client: InvokerClient[UriPackageOrWrapper], resolution_context: IUriResolutionContext[UriPackageOrWrapper]
    ) -> Uri:
        return self._redirects[uri] if uri in self._redirects else uri
