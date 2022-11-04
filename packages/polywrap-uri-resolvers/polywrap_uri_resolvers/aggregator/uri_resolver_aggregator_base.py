from abc import ABC, abstractmethod
from typing import List

from polywrap_core import UriResolutionResult, IUriResolutionStep, IUriResolver, Uri, IUriResolutionContext, Client, UriPackageOrWrapper
from polywrap_result import Result

class UriResolverAggregatorBase(IUriResolver, ABC):
    @abstractmethod
    async def get_uri_resolvers(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result[List[IUriResolver]]:
        pass

    @abstractmethod
    def get_step_description(self) -> str:
        pass

    async def try_resolve_uri(
        self, uri: Uri, client: Client, resolution_context: IUriResolutionContext
    ) -> Result["UriPackageOrWrapper"]:
        resolvers_result = self.get_uri_resolvers(uri, client, resolution_context)

        if resolvers_result.is_err():
            return resolvers_result

        return await self.try_resolve_uri_with_resolvers(
            uri,
            client,
            resolvers_result.value,
            resolution_context
        )


    async def try_resolve_uri_with_resolvers(self, uri: Uri, client: Client, resolvers: List[IUriResolver], resolution_context: IUriResolutionContext) -> Result["UriPackageOrWrapper"]:
        sub_context = resolution_context.create_sub_history_context()

        for resolver in resolvers:
            result = await resolver.try_resolve_uri(uri, client, sub_context)

            if not (result.is_ok() and not hasattr(result.value, 'wrapper') and not hasattr(result.value, 'package') and result.value.uri.uri == uri.uri):
                step = IUriResolutionStep(
                    source_uri=uri,
                    result=result,
                    sub_history=sub_context.get_history(),  # type: ignore
                    description=self.get_step_description() # type: ignore
                )
                resolution_context.track_step(step)

                return result

        result = UriResolutionResult.ok(uri)

        step = IUriResolutionStep(
            source_uri=uri,
            result=result,
            sub_history=sub_context.get_history(),  # type: ignore
            description=self.get_step_description() # type: ignore
        )
        resolution_context.track_step(step)

        return result
