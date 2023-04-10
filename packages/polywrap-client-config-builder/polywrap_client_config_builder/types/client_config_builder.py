"""This module contains the client config builder class."""
# pylint: disable=too-many-public-methods
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from polywrap_core import (
    ClientConfig,
    Env,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
    WrapPackage,
    Wrapper,
)

from .build_options import BuildOptions
from .builder_config import BuilderConfig


class ClientConfigBuilder(ABC):
    """Defines the interface for the client config builder."""

    config: BuilderConfig

    @abstractmethod
    def build(self, options: Optional[BuildOptions] = None) -> ClientConfig:
        """Build the ClientConfig object from the builder's config."""

    @abstractmethod
    def add(self, config: BuilderConfig) -> "ClientConfigBuilder":
        """Add the values from the given config to the builder's config."""

    # ENV CONFIGURE

    @abstractmethod
    def get_env(self, uri: Uri) -> Union[Env, None]:
        """Return the env for the given uri."""

    @abstractmethod
    def get_envs(self) -> Dict[Uri, Env]:
        """Return the envs from the builder's config."""

    @abstractmethod
    def set_env(self, uri: Uri, env: Env) -> "ClientConfigBuilder":
        """Set the env by uri in the builder's config, overiding any existing values."""

    @abstractmethod
    def set_envs(self, uri_envs: Dict[Uri, Env]) -> "ClientConfigBuilder":
        """Set the envs in the builder's config, overiding any existing values."""

    @abstractmethod
    def add_env(self, uri: Uri, env: Env) -> "ClientConfigBuilder":
        """Add an env for the given uri.

        If an Env is already associated with the uri, it is modified.
        """

    @abstractmethod
    def add_envs(self, uri_envs: Dict[Uri, Env]) -> "ClientConfigBuilder":
        """Add a list of envs to the builder's config."""

    @abstractmethod
    def remove_env(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the env for the given uri."""

    @abstractmethod
    def remove_envs(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the envs for the given uris."""

    # INTERFACE IMPLEMENTATIONS CONFIGURE

    @abstractmethod
    def get_interfaces(self) -> Dict[Uri, List[Uri]]:
        """Return all registered interface and its implementations from the builder's config."""

    @abstractmethod
    def get_interface_implementations(self, uri: Uri) -> Union[List[Uri], None]:
        """Return the interface for the given uri."""

    @abstractmethod
    def add_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ) -> "ClientConfigBuilder":
        """Add a list of implementation URIs for the given interface URI to the builder's config."""

    @abstractmethod
    def remove_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ) -> "ClientConfigBuilder":
        """Remove the implementations for the given interface uri."""

    @abstractmethod
    def remove_interface(self, interface_uri: Uri) -> "ClientConfigBuilder":
        """Remove the interface for the given uri."""

    # PACKAGE CONFIGURE

    @abstractmethod
    def get_package(self, uri: Uri) -> Union[WrapPackage[UriPackageOrWrapper], None]:
        """Return the package for the given uri."""

    @abstractmethod
    def get_packages(self) -> Dict[Uri, WrapPackage[UriPackageOrWrapper]]:
        """Return the packages from the builder's config."""

    @abstractmethod
    def set_package(
        self, uri: Uri, package: WrapPackage[UriPackageOrWrapper]
    ) -> "ClientConfigBuilder":
        """Set the package by uri in the builder's config, overiding any existing values."""

    @abstractmethod
    def set_packages(
        self, uri_packages: Dict[Uri, WrapPackage[UriPackageOrWrapper]]
    ) -> "ClientConfigBuilder":
        """Set the packages in the builder's config, overiding any existing values."""

    @abstractmethod
    def remove_package(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the package for the given uri."""

    @abstractmethod
    def remove_packages(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the packages for the given uris."""

    # REDIRECT CONFIGURE

    @abstractmethod
    def get_redirect(self, uri: Uri) -> Union[Uri, None]:
        """Return the redirect for the given uri."""

    @abstractmethod
    def get_redirects(self) -> Dict[Uri, Uri]:
        """Return the redirects from the builder's config."""

    @abstractmethod
    def set_redirect(self, from_uri: Uri, to_uri: Uri) -> "ClientConfigBuilder":
        """Set the redirect from a URI to another URI in the builder's config,\
            overiding any existing values."""

    @abstractmethod
    def set_redirects(self, uri_redirects: Dict[Uri, Uri]) -> "ClientConfigBuilder":
        """Set the redirects in the builder's config, overiding any existing values."""

    @abstractmethod
    def remove_redirect(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the redirect for the given uri."""

    @abstractmethod
    def remove_redirects(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the redirects for the given uris."""

    # RESOLVER CONFIGURE

    @abstractmethod
    def get_resolvers(self) -> List[UriResolver]:
        """Return the resolvers from the builder's config."""

    @abstractmethod
    def add_resolver(self, resolver: UriResolver) -> "ClientConfigBuilder":
        """Add a resolver to the builder's config."""

    @abstractmethod
    def add_resolvers(self, resolvers_list: List[UriResolver]) -> "ClientConfigBuilder":
        """Add a list of resolvers to the builder's config."""

    # WRAPPER CONFIGURE

    @abstractmethod
    def get_wrapper(self, uri: Uri) -> Union[Wrapper[UriPackageOrWrapper], None]:
        """Return the set wrapper for the given uri."""

    @abstractmethod
    def get_wrappers(self) -> Dict[Uri, Wrapper[UriPackageOrWrapper]]:
        """Return the wrappers from the builder's config."""

    @abstractmethod
    def set_wrapper(
        self, uri: Uri, wrapper: Wrapper[UriPackageOrWrapper]
    ) -> "ClientConfigBuilder":
        """Set the wrapper by uri in the builder's config, overiding any existing values."""

    @abstractmethod
    def set_wrappers(
        self, uri_wrappers: Dict[Uri, Wrapper[UriPackageOrWrapper]]
    ) -> "ClientConfigBuilder":
        """Set the wrappers in the builder's config, overiding any existing values."""

    @abstractmethod
    def remove_wrapper(self, uri: Uri) -> "ClientConfigBuilder":
        """Remove the wrapper for the given uri."""

    @abstractmethod
    def remove_wrappers(self, uris: List[Uri]) -> "ClientConfigBuilder":
        """Remove the wrappers for the given uris."""
