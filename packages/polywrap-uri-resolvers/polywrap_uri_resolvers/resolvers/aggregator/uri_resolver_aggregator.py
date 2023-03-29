from typing import List, Optional

from polywrap_core import (
    InvokerClient,
    UriResolver,
    Uri,
    UriPackageOrWrapper,
    IUriResolutionContext,
)

from ...types import UriResolutionStep


class UriResolverAggregator(UriResolver):
    __slots__ = ("resolvers", "step_description")

    resolvers: List[UriResolver]
    step_description: Optional[str]

    def __init__(
        self, resolvers: List[UriResolver], step_description: Optional[str] = None
    ):
        self.step_description = step_description or self.__class__.__name__
        self.resolvers = resolvers

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        sub_context = resolution_context.create_sub_history_context()

        for resolver in self.resolvers:
            uri_package_or_wrapper = await resolver.try_resolve_uri(
                uri, client, sub_context
            )
            if uri_package_or_wrapper != uri:
                step = UriResolutionStep(
                    source_uri=uri,
                    result=uri_package_or_wrapper,
                    sub_history=sub_context.get_history(),
                    description=self.step_description,
                )
                resolution_context.track_step(step)
                return uri_package_or_wrapper

        step = UriResolutionStep(
            source_uri=uri,
            result=uri,
            sub_history=sub_context.get_history(),
            description=self.step_description,
        )
        resolution_context.track_step(step)
        return uri
