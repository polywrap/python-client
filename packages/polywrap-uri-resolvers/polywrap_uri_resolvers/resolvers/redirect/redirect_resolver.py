from polywrap_core import InvokerClient, IUriResolutionContext, Uri, UriPackageOrWrapper


from ..abc import ResolverWithHistory


class RedirectResolver(ResolverWithHistory):
    __slots__ = ("from_uri", "to_uri")

    from_uri: Uri
    to_uri: Uri

    def __init__(self, from_uri: Uri, to_uri: Uri) -> None:
        self.from_uri = from_uri
        self.to_uri = to_uri

    def get_step_description(self) -> str:
        return f"Redirect ({self.from_uri} - {self.to_uri})"

    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        return uri if uri != self.from_uri else self.to_uri
