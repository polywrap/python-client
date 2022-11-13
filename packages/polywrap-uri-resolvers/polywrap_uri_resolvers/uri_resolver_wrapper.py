# TODO: properly implement this
from typing import Union
from polywrap_core import Uri, Client, IUriResolutionContext, UriPackageOrWrapper
from polywrap_uri_resolvers import IResolverWithHistory
from polywrap_result import Result

class UriResolverWrapper(IResolverWithHistory):
    implementation_uri: Uri

    def __init__(self, uri: Uri) -> None:
        self.implementation_uri = uri

    def get_step_description(self) -> str:
        return f"ResolverExtension ({self.implementation_uri})"

    async def _try_resolve_uri(
        self, 
        uri: Uri, 
        client: Client, 
        resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        raise NotImplemented


async def try_resolve_uri_with_implementation(
    uri: Uri,
    implementation_uri: Uri,
    client: Client,
    resolution_context: IUriResolutionContext
) -> Result[Union[str, bytes, None]]:
    raise NotImplemented
