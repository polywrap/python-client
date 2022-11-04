from typing import Optional, Union, cast
from polywrap_core import Uri, Client, IUriResolutionContext, UriPackageOrWrapper
from polywrap_uri_resolvers import ResolverWithHistory
from polywrap_result import Result, Ok, Err

class UriResolverWrapper(ResolverWithHistory):
    implementation_uri: Uri

    def __init__(self, uri: Uri) -> None:
        self.implementation_uri = uri

    def get_step_description(self) -> str:
        return super().get_step_description()

    async def _try_resolve_uri(
        self, 
        uri: Uri, 
        client: Client, 
        resolution_context: IUriResolutionContext
    ) -> Result[UriPackageOrWrapper]:
        result = await try_resolve_uri_with_implementation(uri, self.implementation_uri, client, resolution_context)
        
        if result.is_err():
            return cast(Err, result)

        return Ok()



async def try_resolve_uri_with_implementation(
    uri: Uri,
    implementation_uri: Uri,
    client: Client,
    resolution_context: IUriResolutionContext
) -> Result[Optional[Union[str, bytearray]]]:
    return Ok("")