"""This module contains the UriResolverAggregator Resolver."""
from typing import List, Optional

from polywrap_core import (
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
)

from ...types import UriResolutionStep


class UriResolverAggregator(UriResolver):
    """Defines a resolver that aggregates a list of resolvers.
    
    This resolver aggregates a list of resolvers and tries to resolve\
        the uri with each of them. If a resolver returns a value\
        other than the resolving uri, the value is returned.

    Attributes:
        resolvers (List[UriResolver]): The list of resolvers to aggregate.
        step_description (Optional[str]): The description of the resolution\
            step. Defaults to the class name.
    """

    __slots__ = ("resolvers", "step_description")

    resolvers: List[UriResolver]
    step_description: Optional[str]

    def __init__(
        self, resolvers: List[UriResolver], step_description: Optional[str] = None
    ):
        """Initialize a new UriResolverAggregator instance.

        Args:
            resolvers (List[UriResolver]): The list of resolvers to aggregate.
            step_description (Optional[str]): The description of the resolution\
                step. Defaults to the class name.
        """
        self.step_description = step_description or self.__class__.__name__
        self.resolvers = resolvers

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the uri with each of the aggregated\
            resolvers. If a resolver returns a value other than the resolving\
            uri, the value is returned.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use for\
                resolving the URI.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]):\
                The resolution context to update.
        """
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
