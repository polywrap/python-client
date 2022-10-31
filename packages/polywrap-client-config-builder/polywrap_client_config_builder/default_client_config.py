from typing import Any
from polywrap_core import Uri, ClientConfig
from polywrap_uri_resolvers import BaseUriResolver


def get_default_client_config() -> dict:
    return {
        'envs': [
            {
                'uri': Uri(defaultWrappers.graphNode),
                'env': {
                    'provider': "https://api.thegraph.com",
                    },
                },
                {
                'uri': Uri("wrap://ens/ipfs.polywrap.eth"),
                'env': {
                    'provider': defaultIpfsProviders[0],
                    'fallbackProviders': defaultIpfsProviders.slice(1),
                },
          },
        ],
        'resolver': BaseUriResolver
        
        }