# from .client_config import ClientConfig
from polywrap_core import Uri, Env # missing CoreClientConfig, IUriPackage, IUriWrapper, IUriRedirect
#from .base_client_config import BaseClientConfigBuilder
from polywrap_uri_resolvers import BaseUriResolver
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Dict, List
from .client_config import ClientConfig

class IClientConfigBuilder(ABC):
    """Defines the basic interface for the Client Config Builder"""

    # def add(self, config) -> ClientConfig:
    #     """Appends each property of the supplied config object to the corresponding array of the builder's config."""
    #     self.add_envs(config.envs)
    #     pass

    @abstractmethod
    def build(self) -> ClientConfig:
        """Returns a sanitized config object from the builder's config."""
        pass

    # @abstractmethod
    # def build_core_config() -> CoreClientConfig:
    #     pass

    # @abstractmethod
    # def add(config: )

    # @abstractmethod
    # def add_defaults(self) -> IClientConfigBuilder:
    #     """Adds the defaultClientConfig object."""
    #     pass

    @abstractmethod
    def add_env(self, uri: Uri, env: Dict[str, Any]):# -> IClientConfigBuilder:
        pass

    # @abstractmethod
    # def add_envs():
    #     pass

    # @abstractmethod
    # def remove_env():
    #     pass
