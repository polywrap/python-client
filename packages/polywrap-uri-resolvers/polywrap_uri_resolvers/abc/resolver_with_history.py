from abc import ABC, abstractmethod

from polywrap_core import IUriResolver, Uri, IUriResolutionContext, UriPackageOrWrapper
from polywrap_client import PolywrapClient
from polywrap_result import Result


class ResolverWithHistory(ABC, IUriResolver):
    async def try_resolve_uri(self, uri: Uri, client: PolywrapClient, resolution_context: IUriResolutionContext):
        result = await self._try_resolve_uri(uri, client, resolution_context)
        resolution_context.track_step({
            "source_uri": uri,
            "result": result,
            "description": self.get_step_description(uri, result)
        })

        return result

    @abstractmethod
    def get_step_description(self, uri: Uri, result: Result["UriPackageOrWrapper"]):
        pass

    @abstractmethod
    async def _try_resolve_uri(self, uri: Uri, client: PolywrapClient, resolution_context: IUriResolutionContext):
        pass
