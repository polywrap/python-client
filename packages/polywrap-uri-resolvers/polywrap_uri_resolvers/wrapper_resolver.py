from .abc import IResolverWithHistory
from polywrap_core import (
    Uri,
    UriPackageOrWrapper,
    Wrapper,
    UriResolutionResult,
    Client,
    IUriResolutionContext,
)
from polywrap_result import Result


class WrapperResolver(IResolverWithHistory):
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
        if uri != self.uri:
            return UriResolutionResult.ok(uri)
        return UriResolutionResult.ok(uri, None, self.wrapper)
