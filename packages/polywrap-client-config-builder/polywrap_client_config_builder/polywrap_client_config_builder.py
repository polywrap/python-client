"""This module provides a simple builder for building a ClientConfig object."""
# pylint: disable=too-many-ancestors

from typing import Dict, Optional, cast

from polywrap_core import ClientConfig, UriPackage, UriWrapper
from polywrap_uri_resolvers import (
    ExtendableUriResolver,
    InMemoryResolutionResultCache,
    RecursiveResolver,
    ResolutionResultCacheResolver,
    StaticResolver,
    StaticResolverLike,
    UriResolverAggregator,
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
from .types import BuilderConfig, BuildOptions, BundlePackage, ClientConfigBuilder


class PolywrapClientConfigBuilder(
    BaseConfigure,
    EnvConfigure,
    InterfaceConfigure,
    PackageConfigure,
    RedirectConfigure,
    ResolverConfigure,
    WrapperConfigure,
    ClientConfigBuilder,
):
    """Defines the default polywrap client config builder for\
        building a ClientConfig object for the Polywrap Client.

    The PolywrapClientConfigBuilder is used to create a ClientConfig object,\
        which is used to configure the Polywrap Client and its sub-components.\
        PolywrapClientConfigBuilder provides a simple interface for setting\
        the redirects, wrappers, packages, and other configuration options\
        for the Polywrap Client.

    Examples:
        >>> from polywrap_client_config_builder import PolywrapClientConfigBuilder
        >>> from polywrap_uri_resolvers import RecursiveResolver
        >>> from polywrap_core import Uri
        >>> config = (
        ...     PolywrapClientConfigBuilder()
        ...         .set_env(Uri.from_str("test/uri"), {"hello": "world"})
        ...         .add_interface_implementations(
        ...             Uri.from_str("test/interface"), 
        ...             [Uri.from_str("test/impl1"), Uri.from_str("test/impl2")],
        ...         )
        ...         .set_redirect(Uri("test", "from"), Uri("test", "to"))
        ...         .set_env(Uri("test", "to"), {"foo": "bar"})
        ...         .build()
        ... )
        >>> config.envs
        {Uri("test", "uri"): {'hello': 'world'}, Uri("test", "to"): {'foo': 'bar'}}
        >>> config.interfaces
        {Uri("test", "interface"): [Uri("test", "impl1"), Uri("test", "impl2")]}
        >>> isinstance(config.resolver, RecursiveResolver)
        True
    """

    def __init__(self):
        """Initialize the builder's config attributes with empty values."""
        self.config = BuilderConfig(
            envs={}, interfaces={}, resolvers=[], wrappers={}, packages={}, redirects={}
        )
        super().__init__()

    def add_bundle(self, bundles: Dict[str, BundlePackage]) -> ClientConfigBuilder:
        """Add the bundle to the builder's config."""
        for bundle in bundles.values():
            if bundle.package:
                self.set_package(bundle.uri, bundle.package)
            if bundle.implements:
                for interface in bundle.implements:
                    self.add_interface_implementations(interface, [bundle.uri])
            if bundle.redirects_from:
                for redirect in bundle.redirects_from:
                    self.set_redirect(redirect, bundle.uri)
            if bundle.env:
                self.set_env(bundle.uri, bundle.env)
        return cast(ClientConfigBuilder, self)

    def build(self, options: Optional[BuildOptions] = None) -> ClientConfig:
        """Build the ClientConfig object from the builder's config."""
        static_resolver_like = self._build_static_resolver_like()

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
                    options.resolution_result_cache
                    if options and options.resolution_result_cache
                    else InMemoryResolutionResultCache(),
                )
            )
        )

        return ClientConfig(
            envs=self.config.envs,
            interfaces=self.config.interfaces,
            resolver=resolver,
        )

    def _build_static_resolver_like(self) -> StaticResolverLike:
        static_resolver_like = cast(StaticResolverLike, self.config.redirects)

        for uri, wrapper in self.config.wrappers.items():
            static_resolver_like[uri] = UriWrapper(uri=uri, wrapper=wrapper)

        for uri, package in self.config.packages.items():
            static_resolver_like[uri] = UriPackage(uri=uri, package=package)

        return static_resolver_like


__all__ = ["PolywrapClientConfigBuilder"]
