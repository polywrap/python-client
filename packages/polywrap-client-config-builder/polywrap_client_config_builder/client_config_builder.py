from multiprocessing.connection import Client
from polywrap_core.types.env import Env
from typing import Any, Dict, List
from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_core.types.wrapper import Wrapper, WrapperCache
from polywrap_core import Uri, ClientConfig
from polywrap_uri_resolvers import BaseUriResolver

# Replicate this file
# except for plugins, interface, and redirects as they are not yet impl in python
# https://github.com/polywrap/toolchain/blob/origin/packages/js/client-config-builder/src/ClientConfigBuilder.ts

print(ClientConfig)

def sanitize_uri(uri: str | Uri) -> Uri
    """
    This is the Uri.from function of the JS client
    """
    if type(uri) == str:
        return Uri(uri)
    if Uri.is_uri(uri):
        return uri
    
    raise TypeError("Unknown uri type, cannot convert")

class ClientConfigBuilder():
    """
    Used to instantiate the `ClientConfig` object necessary to invoke any wrapper.
    """

    def __init__(self):
        self.envs: List[Env]
        self.resolver: IUriResolver
        # self.plugins:
        # self.interfaces:
        # self.redirects:

    def __config():
        self.envs = []
        self.resolvers = []

    def add(self, config: ClientConfig) -> ClientConfigBuilder:
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

        defaultWrappers = {
            'sha3': "wrap://ens/goerli/sha3.wrappers.eth",
            'uts46': "wrap://ens/goerli/uts46-lite.wrappers.eth",
            'graphNode': "wrap://ens/goerli/graph-node.wrappers.eth",
            }

        defaultIpfsProviders = [
            "https://ipfs.wrappers.io",
            "https://ipfs.io",
        ]

        def get_default_client_config() -> dict[str, object]:
            return {
                'envs': [
                    {
                        'uri': Uri(defaultWrappers['graphNode']),
                        'env': {
                            'provider': "https://api.thegraph.com",
                            },
                        },
                        {
                        'uri': Uri("wrap://ens/ipfs.polywrap.eth"),
                        'env': {
                            'provider': defaultIpfsProviders[0],
                            'fallbackProviders': defaultIpfsProviders[1:],
                        },
                },
                ],
                'resolver': BaseUriResolver
                
                }
        return get_default_client_config()
        

    def add_env(self, uri: Uri | str, env: Record[str, Any] ) -> ClientConfigBuilder:
        """
        see: https://github.com/polywrap/toolchain/blob/b57b1393d1aa5f82f39741d297040f84bf799ff1/packages/js/client-config-builder/src/ClientConfigBuilder.ts#L153-L168
        Function that takes in an environment object and an Uri;
         - It parses the URI
         - If the env is already defined, its values are updated
         - If the env is not defined, the values are added to the end of the Env array
        """
        # if type(uri) == str:
        #     env_uri: Uri = Uri.parse_uri(uri)
        # elif type(uri) == Uri:
        #     env_uri: Uri = uri
        # else:
        #     raise TypeError("uri is not string nor URI")

        env_uri: Uri = sanitize_uri(uri)

        idx = self.__config

        # Uri.equals(x.uri, )

        if idx >= 0:
            self.envs[idx].env = {**self.envs[idx].env, **env,}
        else:
            self.envs.append(Env(uri=env_uri, env=env))
        return self

    def add_envs(self, envs: list[Env]) -> object:
        for env in envs:
            self.add_envs(env.uri, env.env)
        return self

    def remove_env(self, uri: Uri | str ):
        # very similar to add_env
        pass

    def set_env(self, uri: Uri | str, env: Dict[str, Any] ):     
        # very similar to add_env
        pass

    def set_resolver(self, resolver: IUriResolver):
        self.resolver = resolver
        return self


    def build(self) -> ClientConfig:
        """
        Returns a sanitized config object from the builder's config.
        """

        if not self.resolver:
            raise Exception('No Uri Resolver provided')
        
        pass

    def build_partial(self):
        return self._config