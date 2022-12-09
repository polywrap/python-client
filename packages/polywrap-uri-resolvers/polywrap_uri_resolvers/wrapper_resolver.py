from .abc.resolver_with_history import IResolverWithHistory
from polywrap_core import (
    Uri,
    UriPackageOrWrapper,
    Wrapper,
    Client,
    IUriResolutionContext,
)
from polywrap_result import Result, Ok


class WrapperResolver(IResolverWithHistory):
    __slots__ = ("uri", "wrapper")

    uri: Uri
    wrapper: Wrapper

    def __init__(self, uri: Uri, wrapper: Wrapper):
        self.uri = uri
        self.wrapper = wrapper

    def get_step_description(self) -> str:
        return f"Wrapper ({self.uri})"

    async def _try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        return Ok(uri) if uri != self.uri else Ok(self.wrapper)
