from abc import ABC, abstractmethod
from typing import List

from polywrap_core import IUriResolutionStep, IUriResolver, Uri, IUriResolutionContext, Client, UriPackageOrWrapper
from polywrap_result import Result, Ok

class UriResolverAggregatorBase(ABC, IUriResolver):
    def __init__(self):
        pass

    @abstractmethod
    def get_uri_resolvers(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext):
        pass

    @abstractmethod
    def get_step_description(self):
        pass

    async def try_resolve_uri(self, uri: Uri, client: Client, resolution_context: IUriResolutionContext) -> Result["UriPackageOrWrapper"]:
        pass

    async def try_resolve_uri_with_resolvers(self, uri: Uri, client: Client, resolvers: List[IUriResolver], resolution_context: IUriResolutionContext) -> Result["UriPackageOrWrapper"]:
        sub_context = resolution_context.create_sub_history_context()

        for resolver in resolvers:
            result = await resolver.try_resolve_uri(uri, client, sub_context)
        
            if result.is_err():
                step = IUriResolutionStep(
                    source_uri=uri,
                    result=result,
                    sub_history=sub_context.get_history(),  # type: ignore
                    description=self.get_step_description(uri, result) # type: ignore
                )
                resolution_context.track_step(step)

                return result

            
        result = Ok()

