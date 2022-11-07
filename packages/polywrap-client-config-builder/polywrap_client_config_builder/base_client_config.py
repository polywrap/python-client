from .client_config import ClientConfig
from .interface_client_config_builder import IClientConfigBuilder
from polywrap_core.types.uri import Uri
from polywrap_core.types.env import Env
from typing import Any, Dict, List

#from .client_config_builder import ClientConfigBuilder



class BaseClientConfigBuilder(IClientConfigBuilder):
    """A concrete class of the Client Config Builder, which uses the IClientConfigBuilder Abstract Base Class"""

    def __init__(self):
        self.config: Dict[str, list[Env]] = {
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



    def update_env(self, new_env: Env):
        """
        Takes an Env class as input.(made of an uri and env variables)
        If the env is already defined, its values are updated
        If the env is not defined, raises an error
        """
        # check the envs array and new env you want to load 
        print('loaded_envs', self.config['envs'])
        print('new_env', new_env)

        # Check if both Envs have the same URI
        all_uris: List[Uri | str] = []
        for e in self.config['envs']:
            all_uris.append(e.uri)

        idx = all_uris.index(new_env.uri)

        if idx >= 0:
            print("env already loaded in the envs array, updating")
            self.config['envs'][idx] = new_env
            return self
        else:
            print("env not loaded previously in the loaded_envs array, adding it for the first time")
            # raise Exception("The Uri env has not been defined in the config")
            return self.config['envs'].append(Env(uri=new_env.uri, env=new_env.env))
        
        
        print(update_env())
        assert False
        

    def add_env(self, uri: Uri, env: Dict[str, Any]): #: Record[str, Any] ) -> ClientConfigBuilder:
        """
        see: https://github.com/polywrap/toolchain/blob/b57b1393d1aa5f82f39741d297040f84bf799ff1/packages/js/client-config-builder/src/ClientConfigBuilder.ts#L153-L168
        Function that takes in an environment object and an Uri;
         - It parses the URI
         - If the env is already defined, its values are updated
         - If the env is not defined, the values are added to the end of the Env array
        """
        env_uri: Uri = self.sanitize_uri(uri)
        self.config['envs'].append(Env(uri=env_uri, env=env))
        return self
        

        # for client_env in self.config['envs']:
        #     print('here  is the error', client_env)
        #     if client_env.env == env_uri:
        #         print('this URI already exists in the config, and updating the env:', env_uri)
        #         index = client_env['env'].index(client_env)
        #         client_env['env'][index] = env                                
        #         return self
        #     try:
        #         print(self.config['envs'].index(Env(uri=env_uri, env=env)))
        #         print("env already exists, updating")
        #     except ValueError:
        #         self.config['envs'].append(Env(uri=env_uri, env=env))








        #self.config['envs'].append(Env(uri=env_uri, env=env) )
        
        #idx = self._config


        # Uri.equals(x.uri, )

        # if idx >= 0:
        #     self.envs[idx].env = {**self.envs[idx].env, **env,}
        # else:
        #     self.envs.append(Env(uri=env_uri, env=env))
        return self

    def add_envs(self, envs: list[Env]) -> object:
        for env in envs:
            pass
            self.config['envs'][env.env] = env.uri
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
    
