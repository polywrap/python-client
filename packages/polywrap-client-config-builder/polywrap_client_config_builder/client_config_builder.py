"""
Polywrap Python Client.

The ClientConfigBuilder Package provides a simple interface for building a ClientConfig object,
which is used to configure the Polywrap Client and its sub-components. You can use the
ClientConfigBuilder to set the wrappers, packages, and other configuration options for the
Polywrap Client.

docs.polywrap.io
Copyright 2022 Polywrap
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Union

from polywrap_core import Env, Uri, UriPackage, UriWrapper

UriResolverLike = Union[Uri, UriPackage, UriWrapper, List["UriResolverLike"]]


@dataclass(slots=True, kw_only=True)
class ClientConfig:
    """
    Abstract class used to configure the polywrap client before it executes a call.

    The ClientConfig class is created and modified with the ClientConfigBuilder module.
    """

    envs: Dict[Uri, Dict[str, Any]]
    interfaces: Dict[Uri, List[Uri]]
    wrappers: List[UriWrapper]
    packages: List[UriPackage]
    resolver: List[UriResolverLike]
    redirects: Dict[Uri, Uri]


class BaseClientConfigBuilder(ABC):
    """
    An abstract base class of the `ClientConfigBuilder`.

    It uses the ABC module to define the methods that can be used to
    configure the `ClientConfig` object.
    """

    def __init__(self):
        """Initialize the builder's config attributes with empty values."""
        self.config = ClientConfig(
            envs={}, interfaces={}, resolver=[], wrappers=[], packages=[], redirects={}
        )

    @abstractmethod
    def build(self) -> ClientConfig:
        """Return a sanitized config object from the builder's config."""

    def add(self, new_config: ClientConfig):
        """
        Return a sanitized config object from the builder's config.

        Input is a partial `ClientConfig` object.
        """
        if new_config.envs:
            self.config.envs.update(new_config.envs)
        if new_config.interfaces:
            self.config.interfaces.update(new_config.interfaces)
        if new_config.resolver:
            self.config.resolver.extend(new_config.resolver)
        if new_config.wrappers:
            self.config.wrappers.extend(new_config.wrappers)
        if new_config.packages:
            self.config.packages.extend(new_config.packages)
        return self

    def get_envs(self) -> Dict[Uri, Dict[str, Any]]:
        """Return the envs dictionary from the builder's config."""
        return self.config.envs

    def set_env(self, env: Env, uri: Uri):
        """Set the envs dictionary in the builder's config, overiding any existing values."""
        self.config.envs[uri] = env
        return self

    def add_env(self, env: Env, uri: Uri):
        """
        Add an environment (in the form of an `Env`) for a given uri.

        Note it is not overwriting existing environments, unless the
        env key already exists in the environment, then it will overwrite the existing value.
        """
        if uri in self.config.envs.keys():
            for key in env.keys():
                self.config.envs[uri][key] = env[key]
        else:
            self.config.envs[uri] = env
        return self

    def add_envs(self, envs: List[Env], uri: Uri = None):
        """Add a list of environments (each in the form of an `Env`) for a given uri."""
        for env in envs:
            self.add_env(env, uri)
        return self

    def add_interface_implementations(
        self, interface_uri: Uri, implementations_uris: List[Uri]
    ):
        """Add a list of implementations (each in the form of an `Uri`) for a given interface."""
        if interface_uri is None:
            raise ValueError()
        if interface_uri in self.config.interfaces.keys():
            self.config.interfaces[interface_uri] = (
                self.config.interfaces[interface_uri] + implementations_uris
            )
        else:
            self.config.interfaces[interface_uri] = implementations_uris
        return self

    def add_wrapper(self, wrapper_uri: UriWrapper):
        """Add a wrapper to the list of wrappers."""
        self.config.wrappers.append(wrapper_uri)
        return self

    def add_wrappers(self, wrappers_uris: List[UriWrapper]):
        """Add a list of wrappers to the list of wrappers."""
        for wrapper_uri in wrappers_uris:
            self.add_wrapper(wrapper_uri)
        return self

    def remove_wrapper(self, wrapper_uri: UriWrapper):
        """Remove a wrapper from the list of wrappers."""
        self.config.wrappers.remove(wrapper_uri)
        return self

    def set_package(self, uri_package: UriPackage):
        """Set the package in the builder's config, overiding any existing values."""
        self.config.packages = [uri_package]
        return self

    def add_package(self, uri_package: UriPackage):
        """Add a package to the list of packages."""
        self.config.packages.append(uri_package)
        return self

    def add_packages(self, uri_packages: List[UriPackage]):
        """Add a list of packages to the list of packages."""
        for uri_package in uri_packages:
            self.add_package(uri_package)
        return self

    def remove_package(self, uri_package: UriPackage):
        """Remove a package from the list of packages."""
        self.config.packages.remove(uri_package)
        return self

    def set_resolver(self, uri_resolver: UriResolverLike):
        """Set a single resolver for the `ClientConfig` object."""
        self.config.resolver = [uri_resolver]
        return self

    def add_resolver(self, resolver: UriResolverLike):
        """Add a resolver to the list of resolvers."""
        if self.config.resolver is None:
            raise ValueError(
                "This resolver is not set. Please set a resolver before adding resolvers."
            )
        self.config.resolver.append(resolver)
        return self

    def add_resolvers(self, resolvers_list: List[UriResolverLike]):
        """Add a list of resolvers to the list of resolvers."""
        for resolver in resolvers_list:
            self.add_resolver(resolver)
        return self

    def set_uri_redirect(self, uri_from: Uri, uri_to: Uri):
        """
        Set an uri redirect, from one uri to another.

        If there was a redirect previously listed, it's changed to the new one.
        """
        self.config.redirects[uri_from] = uri_to
        return self

    def remove_uri_redirect(self, uri_from: Uri):
        """Remove an uri redirect, from one uri to another."""
        self.config.redirects.pop(uri_from)
        return self

    def set_uri_redirects(self, redirects: List[Dict[Uri, Uri]]):
        """Set various Uri redirects from a list simultaneously."""
        count = 0
        for redir in redirects:
            for key, value in redir.items():
                self.set_uri_redirect(key, value)
            count += 1
        return self


class ClientConfigBuilder(BaseClientConfigBuilder):
    """
    A class that can build the `ClientConfig` object.

    This class inherits the `BaseClientConfigBuilder` class,
    and adds the `build` method
    """

    def build(self) -> ClientConfig:
        """Return a sanitized config object from the builder's config."""
        return self.config
