from multiprocessing.connection import Client
from typing import List
from polywrap_core.types.env import Env
from polywrap_core.types.uri import Uri
from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_client_config_builder import ClientConfigBuilder
import pytest

test_envs: List[Env] = [
    Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'test': "value" }),
    Env(uri = Uri("wrap://ens/test.plugin.two"), env = { 'test': "value" }),
  ]

client = ClientConfigBuilder()

def test_client_config_builder_adds_envs(test_envs: List[Env]):
    print(client)
    for env in test_envs:
        print('adding an env', env)
        client.add_env(env.uri, env.env)
    
    print(client)
    return client

def test_client_config_builder_adds_default_config():
    print(client.build_partial())
    # print(client.add_defaults().build_partial())
    print(type(client.build_partial()))
    print(client.envs)
    print(type(client.build()))

    assert False

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