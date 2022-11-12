from polywrap_core.types.env import Env
from typing import Any, Dict, List
#from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_core.types.wrapper import Wrapper, WrapperCache
from polywrap_core import Uri, ClientConfig
from polywrap_uri_resolvers import BaseUriResolver
from .base_client_config_builder import BaseClientConfigBuilder

# from bundles import get_default_config
#from base_client_config_builder import base_client_config_builder
# from polywrap_core import Uri, IUriResolver 
#from polywrap_core import core_client_config -> doesnt exist in python client


# from polywrap_uri_resolvers import  IWrapperCache, LegacyRedirectsResolver,  PackageToWrapperCacheResolver,  RecursiveResolver, StaticResolver, WrapperCache
from polywrap_uri_resolvers import BaseUriResolver


# Replicate this file
# except for plugins, interface, and redirects as they are not yet impl in python
# https://github.com/polywrap/toolchain/tree/origin-0.10-dev/packages/js/client-config-builder/src
print(ClientConfig)

class ClientConfigBuilder(BaseClientConfigBuilder):
    """
    Used to instantiate the `ClientConfig` object necessary to invoke any wrapper.
    """
    # config: ClientConfig
   
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
        
