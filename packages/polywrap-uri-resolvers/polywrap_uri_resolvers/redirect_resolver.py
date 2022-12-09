from .abc.resolver_with_history import IResolverWithHistory
from polywrap_core import (
    Uri,
    UriPackageOrWrapper,
    Client,
    IUriResolutionContext,
)
from polywrap_result import Result, Ok


class RedirectResolver(IResolverWithHistory):
    __slots__ = ("from_uri", "to_uri")

    from_uri: Uri
    to_uri: Uri

    def __init__(self, from_uri: Uri, to_uri: Uri) -> None:
        self.from_uri = from_uri
        self.to_uri = to_uri

    def get_step_description(self) -> str:
        return f"Redirect ({self.from_uri} - {self.to_uri})"

    async def _try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        return Ok(uri) if uri != self.from_uri else Ok(self.to_uri)
