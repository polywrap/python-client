from client_config import ClientConfig

from polywrap_core import Uri, Env # missing CoreClientConfig, IUriPackage, IUriWrapper, IUriRedirect

from polywrap_uri_resolvers import BaseUriResolver
from abc import ABC, abstractmethod


class IClientConfigBuilder(ABC):
    """Defines the basic interface for the Client Config Builder"""
    
    @abstractmethod
    def build() -> ClientConfig[Uri]:
        pass

    @abstractmethod
    def build_core_config() -> CoreClientConfif :
        pass

    # @abstractmethod
    # def add(config: )

    @abstractmethod
    def add_defaults() -> IClientConfigBuilder:
        pass

    @abstractmethod
    def add_env():
        pass

    @abstractmethod
    def add_envs():
        pass

    @abstractmethod
    def remove_env():
        pass
