from polywrap_core import Uri, ClientConfig
from dataclasses import dataclass

from polywrap_core.types.env import Env
from typing import Any, Dict, List

from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_core.types.wrapper import Wrapper, WrapperCache

# from "./bundles" import get_default_client_config

# Replicate this file
# except for plugins, interface, and redirects as they are not yet impl in python
# https://github.com/polywrap/toolchain/blob/origin/packages/js/client-config-builder/src/ClientConfigBuilder.ts

print(ClientConfig)

@dataclass(slots=True, kw_only=True)
class ClientConfigBuilder():
    """
    Used to instantiate the `ClientConfig` object necessary to invoke any wrapper.
    """
    envs: List[Env]
    resolver: IUriResolver
    # plugins:
    # interfaces
    # redirects

    def add(self, config: ClientConfig):
        """
        Appends each property of the supplied config object to the corresponding array of the builder's config.
        """
        if config.envs:
            for env in config.envs:
               self.add_env(env.uri, env.env)
        
        if config.resolver:
            self.set_resolver(config.resolver)

        return self

    def add_defaults(self, wrapper_cache: WrapperCache | Any ={'blank': Wrapper}):
        """
        Adds the defaultClientConfig object.
        """
        pass

    def add_env(self, uri: Uri | str, env: Dict[str, Any] ):
        """
        Function that takes in an environment and an Uri;
         - If the env is already defined, its values are updated
         - If the env is not defined, the values are added to the Env array
        """
        env_uri = Uri.parse_uri(uri)
        
        Uri.equals(x.uri, env_uri)

        idx = self.envs.index()
        
        if idx >= 0:
            self.envs[idx].env = {**self.envs[idx].env, **env,}
        else:
            self.envs.append(Env(uri=env_uri, env=env))
        return self

    def remove_env(self, uri: Uri | str ):
        pass

    def set_env(self, uri: Uri | str, env: Dict[str, Any] ):     
        pass

    def set_resolver(self, resolver: IUriResolver):
        pass


    def build(self):
        """
        Returns a sanitized config object from the builder's config.
        """
        pass