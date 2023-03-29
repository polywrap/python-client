from abc import abstractmethod

from polywrap_core import (
    IUriResolutionContext,
    InvokerClient,
    UriResolver,
    Uri,
    UriPackageOrWrapper,
)

from ...types import UriResolutionStep


class ResolverWithHistory(UriResolver):
    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ):
        result = await self._try_resolve_uri(uri, client, resolution_context)
        step = UriResolutionStep(
            source_uri=uri, result=result, description=self.get_step_description()
        )
        resolution_context.track_step(step)

        return result

    @abstractmethod
    def get_step_description(self) -> str:
        pass

    @abstractmethod
    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        pass
