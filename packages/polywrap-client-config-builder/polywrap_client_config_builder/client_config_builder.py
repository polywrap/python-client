from abc import ABC, abstractmethod
from dataclasses import dataclass
from polywrap_core import Uri, IUriResolver, Env
from typing import Dict, Any, List, Optional, Union

@dataclass(slots=True, kw_only=True) 
class ClientConfig():
    """
    This Abstract class is used to configure the polywrap client before it executes a call
    The ClientConfig class is created and modified with the ClientConfigBuilder module
    """
    envs: Dict[Uri, Dict[str, Any]]
    interfaces: Dict[Uri, List[Uri]]
    resolver: IUriResolver
    wrappers: List[Uri]


class IClientConfigBuilder(ABC):
    """
    Interface used by the BaseClientConfigBuilder class. 
    This interface is used to configure the polywrap client before it executes a call
    It defines the methods that can be used to configure the ClientConfig object.
    """

    @abstractmethod
    def build() -> ClientConfig:
        """Returns a sanitized config object from the builder's config."""
        pass

    def get_envs(self) -> Optional[Dict[Uri, Dict[str, Any]]]:
        """Returns the envs dictionary from the builder's config."""
        pass

    @abstractmethod
    def set_env(self, env: Dict[str, Any], uri: Uri):
        pass

    @abstractmethod
    def add_env(self, env: Dict[str, Any], uri: Uri):
        pass

    @abstractmethod
    def add_envs(self, envs: List[Env], uri: Uri):
        pass

    @abstractmethod
    def add_interface_implementations(self, interface_uri: Uri, implementations_uris: List[Uri]):
        pass

    @abstractmethod
    def add_wrapper(self, wrapper_uri: Uri) -> ClientConfig:
        pass

    @abstractmethod
    def add_wrappers(self, wrapper_uris: Optional[List[Uri]]) -> ClientConfig:
        pass

    @abstractmethod
    def set_resolver(self) -> ClientConfig:
        pass

class BaseClientConfigBuilder(IClientConfigBuilder):
    """A concrete class of the Client Config Builder, which uses the IClientConfigBuilder Abstract Base Class"""
    # config: ClientConfig

    def __init__(self):
        self.config = ClientConfig(envs={}, interfaces={}, resolver=None, wrappers= [])

    def build(self)-> ClientConfig:
        """
        Returns a sanitized config object from the builder's config.
        """
        return self.config

    def get_envs(self)-> Dict[Uri, Dict[str, Any]]:
        return self.config.envs
        
    def set_env(self, env: Env={'test':'tested'}, uri=Uri("wrap://ens/eth.plugin.one"))-> IClientConfigBuilder:
        # TODO:  This is a temporary solution to the problem of the Uri / Env not being able to pass as None initially 
        # should be (self, env: Env=None, uri: Uri=None):  but that causes an error
        if (env or uri) is None:
            raise KeyError("Must provide both an env or uri")
        self.config.envs[uri] = env
        return self

        # for key in self.config.envs[uri].keys():
        #     if key in env.keys():
        #         self.config.envs[uri][key] = env[key]
        #     else:
        #         self.config.envs[uri][key] = None
        # return self

    def add_env(self, env: Env = None , uri: Uri = None)-> IClientConfigBuilder:
        if (env or uri) is None:
            raise KeyError("Must provide both an env or uri")
        self.config.envs[uri] = env
        return self

    def add_envs(self, envs: List[Env]) -> IClientConfigBuilder:
        """
        Adds a list of environments (each in the form of an `Env`) for a given uri
        """
        for env in envs:
            self.add_env(env)
        return self

    def add_interface_implementations(self, interface_uri: Uri, implementations_uris: List[Uri]) -> IClientConfigBuilder:
        """
        Adds a list of implementations (each in the form of an `Uri`) for a given interface
        """
        if interface_uri is None:
            raise ValueError()
        if interface_uri in self.config.interfaces.keys():
            self.config.interfaces[interface_uri] = self.config.interfaces[interface_uri] + implementations_uris
        else:
            self.config.interfaces[interface_uri] = implementations_uris
        return self

    def add_wrapper(self, wrapper_uri: Uri) -> IClientConfigBuilder:
        """
        Adds a wrapper to the list of wrappers
        """
        self.config.wrappers.append(wrapper_uri)
        return self

    def add_wrappers(self, wrappers_uris: List[Uri]) -> IClientConfigBuilder:
        """
        Adds a list of wrappers to the list of wrappers
        """
        for wrapper_uri in wrappers_uris:
            self.add_wrapper(wrapper_uri)
        return self

    def remove_wrapper(self, wrapper_uri: Uri) -> IClientConfigBuilder:
        """
        Removes a wrapper from the list of wrappers
        """
        self.config.wrappers.remove(wrapper_uri)
        return self

    def set_resolver(self, uri_resolver) -> IClientConfigBuilder:
        """
        Sets a single resolver for the `ClientConfig` object before it is built
        """
        self.config.resolver = uri_resolver
        return self

class ClientConfigBuilder(BaseClientConfigBuilder):
   ...
