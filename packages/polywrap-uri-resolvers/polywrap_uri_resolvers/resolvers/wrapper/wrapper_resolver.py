from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    Wrapper,
    UriWrapper
)

from ..abc import ResolverWithHistory


class WrapperResolver(ResolverWithHistory):
    __slots__ = ("uri", "wrapper")

    uri: Uri
    wrapper: Wrapper[UriPackageOrWrapper]

    def __init__(self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]):
        self.uri = uri
        self.wrapper = wrapper

    def get_step_description(self) -> str:
        return f"Wrapper ({self.uri})"

    async def _try_resolve_uri(
        self, uri: Uri, client: InvokerClient[UriPackageOrWrapper], resolution_context: IUriResolutionContext[UriPackageOrWrapper]
    ) -> UriPackageOrWrapper:
        return uri if uri != self.uri else UriWrapper(uri, self.wrapper)
