from .client_config import ClientConfig
from .interface_client_config_builder import IClientConfigBuilder
from polywrap_core.types.uri import Uri
from polywrap_core.types.env import Env
from typing import Any, Dict, List

#from .client_config_builder import ClientConfigBuilder



class BaseClientConfigBuilder(IClientConfigBuilder):
    """A concrete class of the Client Config Builder, which uses the IClientConfigBuilder Abstract Base Class"""

    def __init__(self):
        self.config: Dict[str, list] = {
            'envs': [],
            #'resolvers': []
            }

    def __str__(self) -> str:
        return self.config.__str__()

    @property
    def authority(self) -> str:
        return self.config.authority

    def add(self, config: ClientConfig):# -> ClientConfigBuilder:
        """
        Appends each property of the supplied config object to the corresponding array of the builder's config.
        """
        if config.envs:
            for env in config.envs:
               self.add_env(env.uri, env.env)
        
        # if config.resolver:
        #     self.set_resolver(config.resolver)

        return self


    def add_env(self, uri: Uri, env: Env): #: Record[str, Any] ) -> ClientConfigBuilder:
        """
        see: https://github.com/polywrap/toolchain/blob/b57b1393d1aa5f82f39741d297040f84bf799ff1/packages/js/client-config-builder/src/ClientConfigBuilder.ts#L153-L168
        Function that takes in an environment object and an Uri;
         - It parses the URI
         - If the env is already defined, its values are updated
         - If the env is not defined, the values are added to the end of the Env array
        """

        @staticmethod
        def sanitize_uri(uri: str | Uri) -> Uri:
            """
            This is the Uri.from function of the JS client
            """
            if type(uri) == str:
                return Uri(uri)
            if Uri.is_uri(uri):
                return uri
            raise TypeError("Unknown uri type, cannot convert")

        env_uri: Uri = sanitize_uri(uri)
        print(uri, env)
        print('sanitized uri', env_uri)
        self.config['envs'].append(Env(uri=env_uri, env=env) )
        #idx = self._config

        # Uri.equals(x.uri, )

        # if idx >= 0:
        #     self.envs[idx].env = {**self.envs[idx].env, **env,}
        # else:
        #     self.envs.append(Env(uri=env_uri, env=env))
        return self

    def add_envs(self, envs: list[Env]) -> object:
        for env in envs:
            self.config.envs[env.env] = env.uri
        return self

    def remove_env(self, uri: Uri | str ):
        # very similar to add_env
        pass

    def set_env(self, uri: Uri | str, env: Dict[str, Any] ):     
        # very similar to add_env
        pass

    #def set_resolver(self, resolver: IUriResolver):
    #    self.resolver = resolver
    #    return self


    def build(self) -> ClientConfig:
        """
        Returns a sanitized config object from the builder's config.
        """

        # if not self.resolvers:
        #     raise Exception('No Uri Resolver provided')
        
        pass

    # def build_partial(self):# -> ClientConfigBuilder:
    #     return self._config
    
