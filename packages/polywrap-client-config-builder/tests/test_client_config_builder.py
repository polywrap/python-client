from typing import List
from polywrap_core.types.env import Env
from polywrap_core.types.uri import Uri
from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_client_config_builder import ClientConfigBuilder
import pytest
from pytest import fixture
from polywrap_client_config_builder.client_config import ClientConfig

@fixture
def env_varA():
    return Env(uri = Uri("wrap://ens/eth.plugin.one"), env = { 'color': "yellow", 'size': "large" })

@fixture
def env_varB():
    return Env(uri = Uri("wrap://ens/eth.plugin.one"), env = { 'color': "green", 'size': "medium" })

@fixture
def env_varC():
    return Env(uri = Uri("wrap://ens/eth.plugin.one"), env = { 'color': "red", 'size': "small" })

@fixture
def env_varM():
    return Env(uri = Uri("wrap://ens/ipfs.plugin.two"), env = { 'dog': "poodle", 'cat': "siamese" })

@fixture
def env_varN():
    return Env(uri = Uri("wrap://ens/ipfs.plugin.two"), env = { 'dog': "terrier", 'cat': "persian" })

@fixture
def env_varX():
    return Env(uri = Uri("wrap://ens/test.plugin.three"), env = { 'vehicle': "bycicle", 'bird': "parrot", "fruit": "apple" })


def test_client_config_builder_add_env(env_varA, env_varB):
    client_config = ClientConfigBuilder() # instantiate new client config builder
    for env in [ env_varA, env_varB ]: # add all the envs to client
        print(env)
        client_config = client_config.add_env(env) 
    client = client_config.build() # build a client

    print(client)
    assert client.get_envs() == {}.update(env_varA).update(env_varM)

# def test_client_config_builder_add_env_updates_env():
#     client = client.add_env(env_varA.uri, env_varB.env)
#     print(client)
#     assert True # assert client.config['envs'] == 

# def test_client_add_envs():
#     client_config: ClientConfigBuilder = ClientConfigBuilder() # instantiate new client config builder
#     for env in test_envs3: 
#         print("adding env: ", env)
#         client_config = client_config.add_env(env.uri, env.env)
#     client: ClientConfig = client_config.build()
#     assert client.get_envs() == {
#         Uri("wrap://ens/eth.plugin.one") : { 'color': "red", 'size': "small" },
#         Uri("wrap://ens/ipfs.plugin.two"): { 'dog': "terrier", 'cat': "persian" },
#     }

# def test_client_config_builder_set_env():
#     client = ClientConfigBuilder() # instantiate new client
#     client = client.add_env(env_varB)
#     client.set_env(env_varB) # add basic envs to client
#     print(client.config)
#     assert client.config['envs'] == env_varB

@pytest.mark.skip("not yet implemented")
def test_client_config_builder_set_many_envs():
    # client = ClientConfigBuilder.build() # instantiate new client
    # for new_env in test_envs1: #add basic envs
    #     client = client.add_env(new_env.uri, new_env.env)
    # for new_env in test_envs2: # set the new envs, which should overwrite the old ones
    #     client = client.set_env(new_env)
    # assert client.config['envs'] == [
    #     Env(uri=Uri('wrap://ens/test.plugin.one'), env={'color': 'red', 'size': 'small'}), 
    #     Env(uri=Uri("wrap://ens/test.plugin.two"), env={'dog': 'poodle', 'cat': 'siamese'}), 
    #     Env(uri=Uri("wrap://ens/test.plugin.three"), env={'vehicle': 'bycicle', 'bird': 'parrot', 'fruit': 'apple'})]
    pass

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

@pytest.mark.skip(reason="not implemented yet")
def test_client_config_builder_adds_resolvers():
    """tests that the client config builder can add resolver objects and if they are already in the list, it will update them"""
    client = ClientConfigBuilder() # instantiate new client
    for resolver in test_resolvers1:
        client = client.add_resolver(resolver)
    assert client.config['resolvers'] == test_resolvers1

def test_client_config_builder_adds_uri_resolver():
    pass

@pytest.mark.skip("Not implemented")
def test_client_config_builder_adds_plugin():
    pass