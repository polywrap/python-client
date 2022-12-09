from abc import ABC, abstractmethod

from polywrap_core import (
    Client,
    IUriResolutionContext,
    IUriResolutionStep,
    IUriResolver,
    Uri,
    UriPackageOrWrapper,
)
from polywrap_result import Result


class IResolverWithHistory(IUriResolver, ABC):
    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ):
        result = await self._try_resolve_uri(uri, client, resolution_context)
        step = IUriResolutionStep(
            source_uri=uri, result=result, description=self.get_step_description()
        )
        resolution_context.track_step(step)

        return result

    @abstractmethod
    def get_step_description(self) -> str:
        pass

    @abstractmethod
    async def _try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result["UriPackageOrWrapper"]:
        pass
