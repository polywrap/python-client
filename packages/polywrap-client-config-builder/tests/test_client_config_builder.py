from typing import List
from polywrap_core.types.env import Env
from polywrap_core.types.uri import Uri
from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_client_config_builder import ClientConfigBuilder
import pytest


env_var0 = Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'color': "yellow", 'size': "large" })
env_var1 = Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'color': "green", 'size': "medium" })
env_var2 = Env(uri = Uri("wrap://ens/test.plugin.two"), env = { 'dog': "poodle", 'cat': "siamese" })
env_var3 = Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'color': "red", 'size': "small" })
env_var4 = Env(uri = Uri("wrap://ens/test.plugin.two"), env = { 'dog': "terrier", 'cat': "persian" })
env_var5 = Env(uri = Uri("wrap://ens/test.plugin.three"), env = { 'vehicle': "bycicle", 'bird': "parrot", "fruit": "apple" })

test_envs1: List[Env] = [
    env_var1, env_var2,
  ]

test_envs2: List[Env] = [
    env_var3, env_var5
  ]

test_envs3: List[Env] = [
    env_var1, env_var2, env_var3, env_var4, env_var5
]

def test_client_config_builder_add_env():
    client = ClientConfigBuilder() # instantiate new client
    for env in test_envs1: # add all the envs to client
        client = client.add_env(env.uri, env.env) 
    assert client.get_envs() == test_envs1

    client = client.add_env(env_var0.uri, env_var0.env)
    print(client)
    pass #assert client.config['envs'] == 

def test_client_add_envs():
    client = ClientConfigBuilder() # instantiate new client
    for env in test_envs3: 
        client = client.add_env(env.uri, env.env)
    # assert client.config['envs'] == [
    #         Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'color': "green", 'size': "medium" })
    #         env_var2 = Env(uri = Uri("wrap://ens/test.plugin.two"), env = { 'dog': "poodle", 'cat': "siamese" })
    #         env_var3 = Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'color': "red", 'size': "small" })
    #         env_var4 = Env(uri = Uri("wrap://ens/test.plugin.two"), env = { 'dog': "terrier", 'cat': "persian" })
    #         env_var5
    #     ]

def test_client_config_builder_set_env():
    client = ClientConfigBuilder() # instantiate new client
    client = client.add_env(env_var1.uri, env_var1.env)
    client.set_env(env_var3) # add basic envs to client
    print(client.config)
    assert client.config['envs'] == [env_var3]

def test_client_config_builder_set_many_envs():
    client = ClientConfigBuilder() # instantiate new client
    for new_env in test_envs1: #add basic envs
        client = client.add_env(new_env.uri, new_env.env)
    for new_env in test_envs2: # set the new envs, which should overwrite the old ones
        client = client.set_env(new_env)
    assert client.config['envs'] == [
        Env(uri=Uri('wrap://ens/test.plugin.one'), env={'color': 'red', 'size': 'small'}), 
        Env(uri=Uri("wrap://ens/test.plugin.two"), env={'dog': 'poodle', 'cat': 'siamese'}), 
        Env(uri=Uri("wrap://ens/test.plugin.three"), env={'vehicle': 'bycicle', 'bird': 'parrot', 'fruit': 'apple'})]
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