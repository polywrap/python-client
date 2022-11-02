from .abc import ResolverWithHistory
from polywrap_core import Uri, UriPackageOrWrapper, Wrapper, UriResolutionResult
from polywrap_result import Result


class WrapperResolver(ResolverWithHistory):
    uri: Uri
    wrapper: Wrapper

    def __init__(self, uri: Uri, wrapper: Wrapper):
        self.uri = uri
        self.wrapper = wrapper

    def get_step_description(self) -> str:
        return f'Wrapper ({self.uri.uri})'

    async def _try_resolve_uri(self, uri: Uri) -> Result["UriPackageOrWrapper"]: # type: ignore
        if not uri.uri == self.uri.uri:
            return UriResolutionResult.ok(uri)

        return UriResolutionResult.ok(uri, None, self.wrapper)
