from typing import List, Any, Dict, Union
from polywrap_core import Env
from polywrap_core import  Uri
from polywrap_core import IUriResolver
from polywrap_client_config_builder import ClientConfigBuilder
import pytest
from pytest import fixture
from polywrap_client_config_builder import ClientConfig
from dataclasses import asdict

# Variables 

env_varA = { 'color': "yellow", 'size': "large" }
env_varB = { 'color': "red", 'size': "small" }
env_varM = { 'dog': "corgi", 'season': "autumn" }
env_varN = { 'dog': "poodle", 'season': "summer" }
env_uriX = Uri("wrap://ens/eth.plugin.one")
env_uriY = Uri("wrap://ipfs/filecoin.wrapper.two")


# ENVS 

def test_client_config_builder_set_many_envs():
    ccb = ClientConfigBuilder()
    envs = { env_uriX: env_varA }
    ccb = ccb.set_env( env_varA, env_uriX)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs=envs, interfaces={}, resolver = None, wrappers=[]))

def test_client_config_builder_add_env():
    ccb = ClientConfigBuilder() # instantiate new client config builder
    ccb = ccb.add_env(env = env_varA, uri = env_uriX) # add env to client config builder    
    client_config: ClientConfig = ccb.build() # build a client config object
    print(client_config)
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = None, wrappers=[]))

def test_client_config_builder_add_env_updates_env_value():
    ccb = ClientConfigBuilder() # instantiate new client config builder
    ccb = ccb.add_env(env = env_varA, uri = env_uriX) # add env to client config builder
    client_config: ClientConfig = ccb.build() # build a client config object
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = None, wrappers=[]))
    ccb = ccb.add_env(env = env_varB, uri = env_uriX) # update value of env var on client config builder
    client_config: ClientConfig = ccb.build() # build a new client config object
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varB}, interfaces={}, resolver = None, wrappers=[]))


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

# @pytest.mark.skip("not yet implemented")
# def test_client_config_builder_set_many_envs():
#     # client = ClientConfigBuilder.build() # instantiate new client
#     # for new_env in test_envs1: #add basic envs
#     #     client = client.add_env(new_env.uri, new_env.env)
#     # for new_env in test_envs2: # set the new envs, which should overwrite the old ones
#     #     client = client.set_env(new_env)
#     # assert client.config['envs'] == [
#     #     Env(uri=Uri('wrap://ens/test.plugin.one'), env={'color': 'red', 'size': 'small'}), 
#     #     Env(uri=Uri("wrap://ens/test.plugin.two"), env={'dog': 'poodle', 'cat': 'siamese'}), 
#     #     Env(uri=Uri("wrap://ens/test.plugin.three"), env={'vehicle': 'bycicle', 'bird': 'parrot', 'fruit': 'apple'})]
#     pass

# INTERFACES AND IMPLEMENTATIONS

def test_client_config_builder_adds_interface_implementations():
    ccb = ClientConfigBuilder()
    interfaces_uri = Uri("wrap://ens/eth.plugin.one")
    implementations_uris = [Uri("wrap://ens/eth.plugin.one"), Uri("wrap://ens/eth.plugin.two")]
    ccb = ccb.add_interface_implementations(interfaces_uri, implementations_uris)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={interfaces_uri: implementations_uris}, resolver = None, wrappers=[]))

# WRAPPERS AND PLUGINS

def test_client_config_builder_add_wrapper():
    ccb = ClientConfigBuilder()
    wrapper = Uri("wrap://ens/uni.wrapper.eth")
    ccb = ccb.add_wrapper(wrapper)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = None, wrappers=[wrapper]))


def test_client_config_builder_adds_multiple_wrappers():
    ccb = ClientConfigBuilder()
    wrappers = [Uri("wrap://ens/uni.wrapper.eth"), Uri("wrap://ens/https.plugin.eth")]
    ccb = ccb.add_wrappers(wrappers)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = None, wrappers=wrappers))

def test_client_config_builder_removes_wrapper():
    ccb = ClientConfigBuilder()
    wrapper = Uri("wrap://ens/uni.wrapper.eth")
    ccb = ccb.add_wrapper(wrapper)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = None, wrappers=[wrapper]))
    ccb = ccb.remove_wrapper(wrapper)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = None, wrappers=[]))

# RESOLVER 


@pytest.mark.skip("Should implement IURIResolver interface")
def test_client_config_builder_set_uri_resolver():
    ccb = ClientConfigBuilder()
    resolver =  IUriResolver()
    Uri("wrap://ens/eth.resolver.one")
    ccb = ccb.set_resolver()
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=resolver, wrappers=[]))
    