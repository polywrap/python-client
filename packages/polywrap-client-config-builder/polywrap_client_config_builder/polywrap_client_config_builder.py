"""This module provides a simple builder for building a ClientConfig object."""
# pylint: disable=too-many-ancestors

from typing import Optional, cast

from polywrap_core import ClientConfig, UriPackage, UriWrapper
from polywrap_uri_resolvers import (
    ExtendableUriResolver,
    InMemoryResolutionResultCache,
    RecursiveResolver,
    StaticResolver,
    StaticResolverLike,
    UriResolverAggregator,
    ResolutionResultCacheResolver,
)

from .configures import (
    BaseConfigure,
    EnvConfigure,
    InterfaceConfigure,
    PackageConfigure,
    RedirectConfigure,
    ResolverConfigure,
    WrapperConfigure,
)
from .types import BuilderConfig, BuildOptions


class PolywrapClientConfigBuilder(
    BaseConfigure,
    EnvConfigure,
    InterfaceConfigure,
    PackageConfigure,
    RedirectConfigure,
    ResolverConfigure,
    WrapperConfigure,
):
    """Defines the default polywrap client config builder for\
        building a ClientConfig object for the Polywrap Client.

    The PolywrapClientConfigBuilder is used to create a ClientConfig object,\
        which is used to configure the Polywrap Client and its sub-components.\
        PolywrapClientConfigBuilder provides a simple interface for setting\
        the redirects, wrappers, packages, and other configuration options\
        for the Polywrap Client.
    """

    def __init__(self):
        """Initialize the builder's config attributes with empty values."""
        self.config = BuilderConfig(
            envs={}, interfaces={}, resolvers=[], wrappers={}, packages={}, redirects={}
        )

    def build(self, options: Optional[BuildOptions] = None) -> ClientConfig:
        """Build the ClientConfig object from the builder's config."""
        static_resolver_like = cast(
            StaticResolverLike, self.config.redirects
        )

        for uri, wrapper in self.config.wrappers.items():
            static_resolver_like[uri] = UriWrapper(uri=uri, wrapper=wrapper)

        for uri, package in self.config.packages.items():
            static_resolver_like[uri] = UriPackage(uri=uri, package=package)

        resolver = (
            options.resolver
            if options and options.resolver
            else RecursiveResolver(
                ResolutionResultCacheResolver(
                    UriResolverAggregator(
                        [
                            StaticResolver(static_resolver_like),
                            *self.config.resolvers,
                            ExtendableUriResolver(),
                        ]
                    ),
                    options.wrapper_cache
                    if options and options.wrapper_cache
                    else InMemoryResolutionResultCache(),
                )
            )
        )

        return ClientConfig(
            envs=self.config.envs,
            interfaces=self.config.interfaces,
            resolver=resolver,
        )
