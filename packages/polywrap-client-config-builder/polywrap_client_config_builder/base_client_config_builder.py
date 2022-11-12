from .client_config import ClientConfig
from .interface_client_config_builder import IClientConfigBuilder
from polywrap_core.types.uri import Uri
from polywrap_core.types.env import Env
from typing import Any, Dict, List
from dataclasses import dataclass



# @dataclass
class BaseClientConfigBuilder(IClientConfigBuilder):
    """A concrete class of the Client Config Builder, which uses the IClientConfigBuilder Abstract Base Class"""
    config: ClientConfig

    # def __init__(self):
    #     self.config.envs = {} 
    #     self.config.interfaces = {}
    #     self.config.resolver = None

    def __str__(self) -> str:
        return self.config.__str__()

    # @property
    # def authority(self) -> str:
    #     return self.config.authority

    def add(self, config: ClientConfig):# -> BaseClientConfigBuilder:
        """
        Appends each property of the supplied config object to the corresponding array of the builder's config.
        """
        if config.envs:
            for env in config.envs:
               self.add_env(env.uri, env.env)
        
        # if config.resolver:
        #     self.set_resolver(config.resolver)

        return self



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
                
    def add_env(self, uri: Uri, env: Dict[str, Any]): #: Record[str, Any] ) -> ClientConfigBuilder:
        """
        Function that takes in an environment object and an Uri;
         - It sanitizes the URI
         - If the env is already defined, and the env variables AREN'T included already:
            - It adds the new env variables to the existing env, without modifying the old ones
         - If the env is already defined, and the env variables ARE included already:    
            - It updates the existing env variables with the new values        
         - If the env is not defined, the values are added to the end of the Env array
        """
        env_uri: Uri = self.sanitize_uri(uri)
        self.config.envs.append(Env(uri=env_uri, env=env))
        return self
        

    def add_envs(self, envs: list[Env]) -> object:
        for env in envs:
            pass
            self.config['envs'][env.env] = env.uri
        return self



    def set_env(self, new_env: Env): # todo: rename to set_env
        """
        Takes an Env class as input.(made of an uri and env variables)
         - If the env is already defined, its values are updated and the old ones are deleted
         - If the env is not defined, the values are added to the end of the Env array
        """
        # check the envs array and new env you want to load 
        # print('loaded_envs', self.config['envs'])
        # print('new_env', new_env)

        # Check if both Envs have the same URI
        all_uris: List[Uri | str] = []
        for e in self.config['envs']:
            all_uris.append(e.uri)

        try:
            idx = all_uris.index(new_env.uri)
        except ValueError:
            idx = 'undefined'

        if type(idx) == int:
            print("env already loaded in the envs array, updating by substituring loaded_env for new_env")
            self.config['envs'][idx] = new_env
            return self
        else:
            print("env not loaded previously in the loaded_envs array, adding it for the first time")
            self.config['envs'].append(Env(uri=new_env.uri, env=new_env.env))
            return self

    def remove_env(self, uri: Uri | str ):
        # very similar to add_env
        pass

    # def set_env(self, uri: Uri | str, env: Dict[str, Any] ):     
    #     # very similar to add_env
    #     pass

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
    
