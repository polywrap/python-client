"""This module contains the UriResolverAggregator Resolver."""
from typing import List, Optional

from polywrap_core import InvokerClient, UriResolutionContext, UriResolver

from .uri_resolver_aggregator_base import UriResolverAggregatorBase


class UriResolverAggregator(UriResolverAggregatorBase):
    """Defines a resolver that aggregates a list of resolvers.
    
    This resolver aggregates a list of resolvers and tries to resolve\
        the uri with each of them. If a resolver returns a value\
        other than the resolving uri, the value is returned.

    Args:
        resolvers (List[UriResolver]): The list of resolvers to aggregate.
        step_description (Optional[str]): The description of the resolution\
            step. Defaults to the class name.
    """

    __slots__ = ("_resolvers", "_step_description")

    _resolvers: List[UriResolver]
    _step_description: Optional[str]

    def __init__(
        self, resolvers: List[UriResolver], step_description: Optional[str] = None
    ):
        """Initialize a new UriResolverAggregator instance."""
        self._step_description = step_description or self.__class__.__name__
        self._resolvers = resolvers
        super().__init__()

    def get_step_description(self) -> Optional[str]:
        """Get the description of the resolution step."""
        return self._step_description

    def get_resolvers(
        self, client: InvokerClient, resolution_context: UriResolutionContext
    ) -> List[UriResolver]:
        """Get the list of resolvers to aggregate."""
        return self._resolvers


__all__ = ["UriResolverAggregator"]
