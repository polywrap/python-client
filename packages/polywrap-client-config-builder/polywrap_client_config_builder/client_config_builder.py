"""This module provides a simple builder for building a ClientConfig object."""

from typing import Any, Dict, List, Optional, cast

from polywrap_core import (
    ClientConfig,
    Env,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolver,
    UriWrapper,
    WrapPackage,
    Wrapper,
)
from polywrap_uri_resolvers import (
    ExtendableUriResolver,
    InMemoryWrapperCache,
    PackageToWrapperResolver,
    RecursiveResolver,
    RequestSynchronizerResolver,
    StaticResolver,
    UriResolverAggregator,
    WrapperCacheResolver,
)

from .types import BuilderConfig, BuildOptions


class ClientConfigBuilder:
    """Defines a simple builder for building a ClientConfig object.

    The ClientConfigBuilder is used to create a ClientConfig object,\
        which is used to configure the Polywrap Client and its sub-components.\
        ClientConfigBuilder provides a simple interface for setting\
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
        resolver = (
            options.resolver
            if options and options.resolver
            else RecursiveResolver(
                RequestSynchronizerResolver(
                    WrapperCacheResolver(
                        PackageToWrapperResolver(
                            UriResolverAggregator(
                                [
                                    StaticResolver(self.config.redirects),
                                    StaticResolver(self.config.wrappers),
                                    StaticResolver(self.config.packages),
                                    *self.config.resolvers,
                                    ExtendableUriResolver(),
                                ]
                            )
                        ),
                        options.wrapper_cache
                        if options and options.wrapper_cache
                        else InMemoryWrapperCache(),
                    )
                )
            )
        )

        return ClientConfig(
            envs=self.config.envs,
            interfaces=self.config.interfaces,
            resolver=resolver,
        )

    def add(self, config: BuilderConfig):
        """Add the values from the given config to the builder's config."""
        if config.envs:
            self.config.envs.update(config.envs)
        if config.interfaces:
            self.config.interfaces.update(config.interfaces)
        if config.redirects:
            self.config.redirects.update(config.redirects)
        if config.resolvers:
            self.config.resolvers.extend(config.resolvers)
        if config.wrappers:
            self.config.wrappers.update(config.wrappers)
        if config.packages:
            self.config.packages.update(config.packages)
        return self

    def get_envs(self) -> Dict[Uri, Dict[str, Any]]:
        """Return the envs from the builder's config."""
        return self.config.envs

    def set_env(self, uri: Uri, env: Env):
        """Set the env by uri in the builder's config, overiding any existing values."""
        self.config.envs[uri] = env
        return self

    def set_envs(self, uri_envs: Dict[Uri, Env]):
        """Set the envs in the builder's config, overiding any existing values."""
        self.config.envs.update(uri_envs)
        return self

    def add_env(self, uri: Uri, env: Env):
        """Add an env for the given uri.

        If an Env is already associated with the uri, it is modified.
        """
        if self.config.envs.get(uri):
            for key in self.config.envs[uri]:
                self.config.envs[uri][key] = env[key]
        else:
            self.config.envs[uri] = env
        return self

    def add_envs(self, uri_envs: Dict[Uri, Env]):
        """Add a list of envs to the builder's config."""
        for uri, env in uri_envs.items():
            self.add_env(uri, env)
        return self

    def add_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ):
        """Add a list of implementation URIs for the given interface URI to the builder's config."""
        if interface_uri in self.config.interfaces.keys():
            self.config.interfaces[interface_uri].extend(implementations_uris)
        else:
            self.config.interfaces[interface_uri] = implementations_uris
        return self

    def add_wrapper(self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]):
        """Add a wrapper by its URI to the builder's config."""
        self.config.wrappers[uri] = wrapper
        return self

    def add_wrappers(self, uri_wrappers: List[UriWrapper[UriPackageOrWrapper]]):
        """Add a list of URI-wrapper pairs to the builder's config."""
        for uri_wrapper in uri_wrappers:
            self.add_wrapper(cast(Uri, uri_wrapper), uri_wrapper.wrapper)
        return self

    def remove_wrapper(self, uri: Uri):
        """Remove a wrapper by its URI from the builder's config."""
        del self.config.wrappers[uri]
        return self

    def remove_wrappers(self, uris: List[Uri]):
        """Remove a list of wrappers by its URIs."""
        for uri in uris:
            self.remove_wrapper(uri)
        return self

    def add_package(self, uri: Uri, package: WrapPackage[UriPackageOrWrapper]):
        """Add a package by its URI to the builder's config."""
        self.config.packages[uri] = package
        return self

    def add_packages(self, uri_packages: List[UriPackage[UriPackageOrWrapper]]):
        """Add a list of URI-package pairs to the builder's config."""
        for uri_package in uri_packages:
            self.add_package(cast(Uri, uri_package), uri_package.package)
        return self

    def remove_package(self, uri: Uri):
        """Remove a package by its URI from the builder's config."""
        del self.config.packages[uri]
        return self

    def remove_packages(self, uris: List[Uri]):
        """Remove a list of packages by its URIs from the builder's config."""
        for uri in uris:
            self.remove_package(uri)
        return self

    def add_resolver(self, resolver: UriResolver):
        """Add a resolver to the builder's config."""
        self.config.resolvers.append(resolver)
        return self

    def add_resolvers(self, resolvers_list: List[UriResolver]):
        """Add a list of resolvers to the builder's config."""
        for resolver in resolvers_list:
            self.add_resolver(resolver)
        return self

    def add_redirect(self, from_uri: Uri, to_uri: Uri):
        """Add a URI redirect from `from_uri` to `to_uri`."""
        self.config.redirects[from_uri] = to_uri
        return self

    def remove_redirect(self, from_uri: Uri):
        """Remove a URI redirect by `from_uri`."""
        del self.config.redirects[from_uri]
        return self

    def add_redirects(self, redirects: Dict[Uri, Uri]):
        """Add a list of URI redirects to the builder's config."""
        self.config.redirects.update(redirects)
        return self
