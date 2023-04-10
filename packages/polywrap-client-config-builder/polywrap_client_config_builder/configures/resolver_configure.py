"""This module contains the resolver configure class for the client config builder."""
from typing import List

from polywrap_core import UriResolver

from ..types import ClientConfigBuilder


class ResolverConfigure(ClientConfigBuilder):
    """Allows configuring the URI resolvers."""

    def get_resolvers(self) -> List[UriResolver]:
        """Return the resolvers from the builder's config."""
        return self.config.resolvers

    def add_resolver(self, resolver: UriResolver) -> ClientConfigBuilder:
        """Add a resolver to the builder's config."""
        self.config.resolvers.append(resolver)
        return self

    def add_resolvers(self, resolvers_list: List[UriResolver]) -> ClientConfigBuilder:
        """Add a list of resolvers to the builder's config."""
        for resolver in resolvers_list:
            self.add_resolver(resolver)
        return self
