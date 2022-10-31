from .abc import ResolverWithHistory
from polywrap_core import IUriResolver, Uri, UriPackageOrWrapper, IUriResolutionContext
from polywrap_client import PolywrapClient
from polywrap_result import Result


class WrapperResolver(ResolverWithHistory):
    def __init__(self):
        self.super()

    def get_step_description(self, uri: Uri, result: Result["UriPackageOrWrapper"]):
        pass

    def _try_resolve_uri(self, uri: Uri, client: PolywrapClient, resolution_context: IUriResolutionContext):
        pass


