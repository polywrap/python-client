from typing import List
from polywrap_core.types.env import Env
from polywrap_core.types.uri import Uri
from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_client_config_builder import ClientConfigBuilder
import pytest

test_envs1: List[Env] = [
    Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'color': "green", 'size': "medium" }),
    Env(uri = Uri("wrap://ens/test.plugin.two"), env = { 'dog': "poodle", 'cat': "siamese" }),
  ]

test_envs2: List[Env] = [
    Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'color': "red", 'size': "small" }),
   # Env(uri = Uri("wrap://ens/test.plugin.two"), env = { 'dog': "terrier", 'cat': "persian" }),
    Env(uri = Uri("wrap://ens/test.plugin.three"), env = { 'vehicle': "bycicle", 'bird': "parrot", "fruit": "apple" }),
  ]


def test_client_config_builder_add_env():
    client = ClientConfigBuilder() # instantiate new client
    for env in test_envs1: # add all the envs to client
        client = client.add_env(env.uri, env.env) 
    #print(client.config['envs'])
    assert client.config['envs'] == test_envs1

    for env in test_envs2:
        client = client.add_env(env.uri, env.env)

    print(client.config['envs'])
    assert False


# def test_client_config_builder_adds_default_config():
#     #print(client.build_partial())
#     # print(client.add_defaults().build_partial())
#     #print(type(client.build_partial()))
#     print(client.envs)
#     print(type(client.build()))
#     pass
# def test_client_config_builder_adds_config():
#     envs: List[Env] = []
#     resolver: IUriResolver = IUriResolver()
#     config = ClientConfigBuilder(env).add({})
#     pass

def test_client_config_builder_adds_uri_resolver():
    pass

@pytest.mark.skip("Not implemented")
def test_client_config_builder_adds_plugin():
    pass