from abc import ABC, abstractmethod
from dataclasses import dataclass
from polywrap_core import Uri, IUriResolver, Env
from typing import Dict, Any, List

@dataclass(slots=True, kw_only=True) 
class ClientConfig():
    """
    This Abstract class is used to configure the polywrap client before it executes a call
    The ClientConfig class is created and modified with the ClientConfigBuilder module
    """
    envs: Dict[Uri, Dict[str, Any]]
    interfaces: Dict[Uri, List[Uri]]
    resolver: IUriResolver

#

class IClientConfigBuilder(ABC):

    @abstractmethod
    def build() -> ClientConfig:
        """Returns a sanitized config object from the builder's config."""
        pass

    @abstractmethod
    def set_env() -> ClientConfig:
        pass

    @abstractmethod
    def add_env() -> ClientConfig:
        pass

    @abstractmethod
    def add_envs() -> ClientConfig:
        pass

    # @abstractmethod
    # def add_interface() -> ClientConfig:
    #     pass

    # @abstractmethod
    # def set_resolver() -> ClientConfig:
    #     pass

class BaseClientConfigBuilder(IClientConfigBuilder):
    """A concrete class of the Client Config Builder, which uses the IClientConfigBuilder Abstract Base Class"""
    # config: ClientConfig

    def __init__(self):
        self.config = ClientConfig(envs={}, interfaces={}, resolver=None)

    def build(self):
        """
        Returns a sanitized config object from the builder's config.
        """
        return self.config

    def set_env(self, env=None, uri=None):
        if (env or uri) is None:
            raise KeyError("Must provide both an env or uri")
        self.config.envs[uri]: Env = env
        return self

    def add_env(self, env: Env = None , uri: Uri = None):
        pass

    def add_envs(self, envs): 
        for env in envs:
            self.add_env(env)
        return self

class ClientConfigBuilder(BaseClientConfigBuilder):
   ...
