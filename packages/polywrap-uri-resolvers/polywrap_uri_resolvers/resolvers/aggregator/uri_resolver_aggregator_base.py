"""This module contains the UriResolverAggregator Resolver."""
# pylint: disable=unnecessary-ellipsis
from abc import ABC, abstractmethod
from typing import List, Optional

from polywrap_core import (
    InvokerClient,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolutionContext,
    UriResolutionStep,
    UriResolver,
    UriWrapper,
)


class UriResolverAggregatorBase(UriResolver, ABC):
    """Defines a base resolver that aggregates a list of resolvers.
    
    This resolver aggregates a list of resolvers and tries to resolve\
        the uri with each of them. If a resolver returns a value\
        other than the resolving uri, the value is returned.
    """

    @abstractmethod
    def get_resolvers(
        self, client: InvokerClient, resolution_context: UriResolutionContext
    ) -> List[UriResolver]:
        """Get the list of resolvers to aggregate."""
        ...

    @abstractmethod
    def get_step_description(self) -> Optional[str]:
        """Get the description of the resolution step. Defaults to the class name."""
        ...

    def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient,
        resolution_context: UriResolutionContext,
    ) -> UriPackageOrWrapper:
        """Try to resolve a URI to a wrap package, a wrapper, or a URI.

        This method tries to resolve the uri with each of the aggregated\
            resolvers. If a resolver returns a value other than the resolving\
            uri, the value is returned.
        
        Args:
            uri (Uri): The URI to resolve.
            client (InvokerClient): The client to use for\
                resolving the URI.
            resolution_context (UriResolutionContext):\
                The resolution context to update.
        """
        sub_context = resolution_context.create_sub_history_context()

        for resolver in self.get_resolvers(client, sub_context):
            uri_package_or_wrapper = resolver.try_resolve_uri(uri, client, sub_context)
            if (
                isinstance(uri_package_or_wrapper, (UriPackage, UriWrapper))
                or uri_package_or_wrapper != uri
            ):
                step = UriResolutionStep(
                    source_uri=uri,
                    result=uri_package_or_wrapper,
                    sub_history=sub_context.get_history(),
                    description=self.get_step_description(),
                )
                resolution_context.track_step(step)
                return uri_package_or_wrapper

        step = UriResolutionStep(
            source_uri=uri,
            result=uri,
            sub_history=sub_context.get_history(),
            description=self.get_step_description(),
        )
        resolution_context.track_step(step)
        return uri


__all__ = ["UriResolverAggregatorBase"]
