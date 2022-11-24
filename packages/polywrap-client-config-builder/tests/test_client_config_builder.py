from typing import List, Any, Dict, Union
from polywrap_core import Env
from polywrap_core import  Uri
from polywrap_core import IUriResolver, UriPackage, UriWrapper
from polywrap_client_config_builder import ClientConfigBuilder
import pytest
from pytest import fixture
from polywrap_client_config_builder import ClientConfig
from dataclasses import asdict

# Variables 

env_varA = { 'color': "yellow", 'size': "large" }
env_varB = { 'color': "red", 'size': "small" }
env_varN = { 'dog': "poodle", 'season': "summer" }
env_varM = { 'dog': "corgi", 'season': "autumn" }
env_varN = { 'dog': "poodle", 'season': "summer" }
env_varS = { 'vehicle': "scooter"}
env_uriX = Uri("wrap://ens/eth.plugin.one")
env_uriY = Uri("wrap://ipfs/filecoin.wrapper.two")


# ENVS 

def test_client_config_builder_set_env():
    ccb = ClientConfigBuilder()
    envs = { env_uriX: env_varA }
    ccb = ccb.set_env( env_varA, env_uriX)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs=envs, interfaces={}, resolver = [], wrappers=[], packages=[]))

def test_client_config_builder_add_env():
    ccb = ClientConfigBuilder() # instantiate new client config builder
    ccb = ccb.add_env(env = env_varA, uri = env_uriX) # add env to client config builder    
    client_config: ClientConfig = ccb.build() # build a client config object
    print(client_config)
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = [], wrappers=[], packages=[]))

def test_client_config_builder_add_env_updates_env_value():
    ccb = ClientConfigBuilder() # instantiate new client config builder
    ccb = ccb.add_env(env = env_varA, uri = env_uriX) # add env to client config builder
    client_config: ClientConfig = ccb.build() # build a client config object
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = [], wrappers=[], packages=[]))
    ccb = ccb.add_env(env = env_varB, uri = env_uriX) # update value of env var on client config builder
    client_config: ClientConfig = ccb.build() # build a new client config object
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varB}, interfaces={}, resolver = [], wrappers=[], packages=[]))

def test_client_config_builder_set_env_and_add_env_updates_and_add_values():
    ccb = ClientConfigBuilder()
    ccb = ccb.set_env(env_varA, env_uriX) # set the environment variables A
    client_config: ClientConfig = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varA}, interfaces={}, resolver = [], wrappers=[], packages=[]))

    ccb = ccb.set_env(env_varB, env_uriX) # set new vars on the same Uri
    client_config: ClientConfig = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={env_uriX: env_varB}, interfaces={}, resolver = [], wrappers=[], packages=[]))

    ccb = ccb.add_env(env_varM, env_uriY) # add new env vars on a new Uri
    client_config: ClientConfig = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(
        envs={
            env_uriX: env_varB,
            env_uriY: env_varM
        }, 
        interfaces={}, resolver = [], wrappers=[], packages=[]))

    # add new env vars on the second Uri, while also updating the Env vars of dog and season
    ccb = ccb.add_envs([env_varN, env_varS], env_uriY)
    new_envs = {**env_varM, **env_varN, **env_varS}
    print(new_envs)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs = {env_uriX: env_varB, env_uriY: new_envs}, interfaces={}, resolver = [], wrappers=[], packages=[]))

# INTERFACES AND IMPLEMENTATIONS

def test_client_config_builder_adds_interface_implementations():
    ccb = ClientConfigBuilder()
    interfaces_uri = Uri("wrap://ens/eth.plugin.one")
    implementations_uris = [Uri("wrap://ens/eth.plugin.one"), Uri("wrap://ens/eth.plugin.two")]
    ccb = ccb.add_interface_implementations(interfaces_uri, implementations_uris)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={interfaces_uri: implementations_uris}, resolver = [], wrappers=[], packages=[]))

# PACKAGES

@pytest.mark.skip("Should implement UriPackage interface with package argument")
def test_client_config_builder_set_package():
    ccb = ClientConfigBuilder()
    package = UriPackage(Uri("wrap://ens/uni.wrapper.eth"), version="1.0.0")
    ccb = ccb.set_package(package)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[package]))

@pytest.mark.skip("Should implement UriPackage interface with package argument")
def test_client_config_builder_add_package():
    ccb = ClientConfigBuilder()
    package = UriPackage(Uri("wrap://ens/uni.wrapper.eth"))
    ccb = ccb.add_package(package)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[package]))

@pytest.mark.skip("Should implement UriPackage interface with package argument")
def test_client_config_builder_add_package_updates_package():
    ccb = ClientConfigBuilder()
    package = UriPackage(Uri("wrap://ens/uni.wrapper.eth"))
    ccb = ccb.add_package(package)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[package]))
    package = UriPackage(Uri("wrap://ens/uni.wrapper.eth"))
    ccb = ccb.add_package(package)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[package]))

@pytest.mark.skip("Should implement UriPackage interface with package argument")
def test_client_config_builder_add_packages():
    ccb = ClientConfigBuilder()
    package = UriPackage(Uri("wrap://ens/uni.wrapper.eth"))
    package2 = UriPackage(Uri("wrap://ens/uni.wrapper.eth"))
    ccb = ccb.add_packages([package, package2])
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[package, package2]))

@pytest.mark.skip("Should implement UriPackage interface with package argument")
def test_client_config_builder_add_packages_removes_packages():
    ccb = ClientConfigBuilder()
    package = UriPackage(Uri("wrap://ens/uni.wrapper.eth"))
    package2 = UriPackage(Uri("wrap://ens/uni.wrapper.eth"))
    ccb = ccb.add_packages([package, package2])
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[package, package2]))
    ccb = ccb.remove_package([package1])
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[package2]))

# WRAPPERS AND PLUGINS

def test_client_config_builder_add_wrapper():
    ccb = ClientConfigBuilder()
    wrapper = Uri("wrap://ens/uni.wrapper.eth")
    ccb = ccb.add_wrapper(wrapper)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[wrapper], packages=[]))

def test_client_config_builder_adds_multiple_wrappers():
    ccb = ClientConfigBuilder()
    wrappers = [Uri("wrap://ens/uni.wrapper.eth"), Uri("wrap://ens/https.plugin.eth")]
    ccb = ccb.add_wrappers(wrappers)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=wrappers, packages=[]))

def test_client_config_builder_removes_wrapper():
    ccb = ClientConfigBuilder()
    wrapper = Uri("wrap://ens/uni.wrapper.eth")
    ccb = ccb.add_wrapper(wrapper)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[wrapper], packages=[]))
    ccb = ccb.remove_wrapper(wrapper)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver = [], wrappers=[], packages=[]))

# RESOLVER 

@pytest.mark.skip("Should implement IURIResolver interface")
def test_client_config_builder_set_uri_resolver():
    ccb = ClientConfigBuilder()
    resolver =  IUriResolver()
    Uri("wrap://ens/eth.resolver.one")
    ccb = ccb.set_resolver(resolver)
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[resolver], wrappers=[], packages=[]))
    
def test_client_config_builder_add_resolver():

    # set a first resolver
    ccb = ClientConfigBuilder()
    resolverA = Uri("wrap://ens/eth.resolver.one")
    ccb: ClientConfigBuilder = ccb.set_resolver(resolverA)
    client_config: ClientConfig = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[resolverA], wrappers=[], packages=[]))
    
    # add a second resolver
    resolverB = Uri("wrap://ens/eth.resolver.two")
    ccb = ccb.add_resolver(resolverB)
    client_config: ClientConfig = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=[resolverA, resolverB], wrappers=[], packages=[]))

    # add a third and fourth resolver
    resolverC = Uri("wrap://ens/eth.resolver.three")
    resolverD = Uri("wrap://ens/eth.resolver.four")
    ccb = ccb.add_resolvers([resolverC, resolverD])
    client_config: ClientConfig = ccb.build()
    resolvers = [resolverA, resolverB, resolverC, resolverD]
    assert asdict(client_config) == asdict(ClientConfig(envs={}, interfaces={}, resolver=resolvers, wrappers=[], packages=[]))

# TODO: add tests for the following methods

def test_client_config_builder_generic_add():
    # Test adding package, wrapper, resolver, interface, and env with the ccb.add method
    pass