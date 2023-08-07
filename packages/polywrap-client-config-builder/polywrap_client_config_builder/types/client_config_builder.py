"""This module contains the client config builder class."""
# pylint: disable=too-many-public-methods
from typing import Any, Dict, List, Optional, Protocol, Union

from polywrap_core import ClientConfig, Uri, UriResolver, WrapPackage, Wrapper

from .build_options import BuildOptions
from .builder_config import BuilderConfig
from .bundle_package import BundlePackage


class ClientConfigBuilder(Protocol):
    """Defines the interface for the client config builder."""

    config: BuilderConfig

    def build(self, options: Optional[BuildOptions] = None) -> ClientConfig:
        """Build the ClientConfig object from the builder's config."""
        ...

    def add(self, config: BuilderConfig) -> "ClientConfigBuilder":
        """Add the values from the given config to the builder's config."""
        ...

    # BUNDLE CONFIGURE

    def add_bundle(self, bundles: Dict[str, BundlePackage]) -> "ClientConfigBuilder":
        """Add a bundle to the builder's config."""
        ...

    # ENV CONFIGURE

    def get_env(self, uri: Uri) -> Union[Any, None]:
        """Return the env for the given uri."""
        ...

    def get_envs(self) -> Dict[Uri, Any]:
        """Return the envs from the builder's config."""
        ...

    def set_env(self, uri: Uri, env: Any) -> "ClientConfigBuilder":
        """Set the env by uri in the builder's config, overiding any existing values."""
        ...

    def set_envs(self, uri_envs: Dict[Uri, Any]) -> "ClientConfigBuilder":
        """Set the envs in the builder's config, overiding any existing values."""
        ...

    def add_env(self, uri: Uri, env: Any) -> "ClientConfigBuilder":
        """Add an env for the given uri.

        If an Any is already associated with the uri, it is modified.
        """
        ...

    def add_envs(self, uri_envs: Dict[Uri, Any]) -> "ClientConfigBuilder":
        """Add a list of envs to the builder's config."""
        ...

    def remove_env(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the env for the given uri."""
        ...

    def remove_envs(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the envs for the given uris."""
        ...

    # INTERFACE IMPLEMENTATIONS CONFIGURE

    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        """Return all registered interface and its implementations from the builder's config."""
        ...

    def get_interface_implementations(self, uri: Uri) -> Union[List[Uri], None]:
        """Return the interface for the given uri."""
        ...

    def add_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ) -> "ClientConfigBuilder":
        """Add a list of implementation URIs for the given interface URI to the builder's config."""
        ...

    def remove_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ) -> "ClientConfigBuilder":
        """Remove the implementations for the given interface uri."""
        ...

    def remove_interface(self, interface_uri: Uri) -> "ClientConfigBuilder":
        """Remove the interface for the given uri."""
        ...

    # PACKAGE CONFIGURE

    def get_package(self, uri: Uri) -> Union[WrapPackage, None]:
        """Return the package for the given uri."""
        ...

    def get_packages(self) -> Dict[Uri, WrapPackage]:
        """Return the packages from the builder's config."""
        ...

    def set_package(self, uri: Uri, package: WrapPackage) -> "ClientConfigBuilder":
        """Set the package by uri in the builder's config, overiding any existing values."""
        ...

    def set_packages(
        self, uri_packages: Dict[Uri, WrapPackage]
    ) -> "ClientConfigBuilder":
        """Set the packages in the builder's config, overiding any existing values."""
        ...

    def remove_package(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the package for the given uri."""
        ...

    def remove_packages(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the packages for the given uris."""
        ...

    # REDIRECT CONFIGURE

    def get_redirect(self, uri: Uri) -> Union[Uri, None]:
        """Return the redirect for the given uri."""
        ...

    def get_redirects(self) -> Dict[Uri, Uri]:
        """Return the redirects from the builder's config."""
        ...

    def set_redirect(self, from_uri: Uri, to_uri: Uri) -> "ClientConfigBuilder":
        """Set the redirect from a URI to another URI in the builder's config,\
            overiding any existing values."""
        ...

    def set_redirects(self, uri_redirects: Dict[Uri, Uri]) -> "ClientConfigBuilder":
        """Set the redirects in the builder's config, overiding any existing values."""
        ...

    def remove_redirect(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the redirect for the given uri."""
        ...

    def remove_redirects(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the redirects for the given uris."""
        ...

    # RESOLVER CONFIGURE

    def get_resolvers(self) -> List[UriResolver]:
        """Return the resolvers from the builder's config."""
        ...

    def add_resolver(self, resolver: UriResolver) -> "ClientConfigBuilder":
        """Add a resolver to the builder's config."""
        ...

    def add_resolvers(self, resolvers_list: List[UriResolver]) -> "ClientConfigBuilder":
        """Add a list of resolvers to the builder's config."""
        ...

    # WRAPPER CONFIGURE

    def get_wrapper(self, uri: Uri) -> Union[Wrapper, None]:
        """Return the set wrapper for the given uri."""
        ...

    def get_wrappers(self) -> Dict[Uri, Wrapper]:
        """Return the wrappers from the builder's config."""
        ...

    def set_wrapper(self, uri: Uri, wrapper: Wrapper) -> "ClientConfigBuilder":
        """Set the wrapper by uri in the builder's config, overiding any existing values."""
        ...

    def set_wrappers(self, uri_wrappers: Dict[Uri, Wrapper]) -> "ClientConfigBuilder":
        """Set the wrappers in the builder's config, overiding any existing values."""
        ...

    def remove_wrapper(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the wrapper for the given uri."""
        ...

    def remove_wrappers(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the wrappers for the given uris."""
        ...


__all__ = ["ClientConfigBuilder"]
