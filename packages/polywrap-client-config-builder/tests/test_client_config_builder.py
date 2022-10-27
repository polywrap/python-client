from typing import List
from polywrap_core.types.env import Env
from polywrap_core.types.uri import Uri
from polywrap_core.types.uri_resolver import IUriResolver
from polywrap_client_config_builder import ClientConfigBuilder

test_envs: List[Env] = [
    Env(uri = Uri("wrap://ens/test.plugin.one"), env = { 'test': "value" }),
    Env(uri= Uri("wrap://ens/test.plugin.two"), env= { 'test': "value" }),
  ]

def test_client_config_builder_adds_default_config():
    ClientConfigBuilder.add_defaults()
    pass

def test_client_config_builder_adds_config():
    envs: List[Env] = []
    resolver: IUriResolver = IUriResolver()


    config = ClientConfigBuilder(env).add({})
    pass

def test_client_config_builder_adds_uri_resolver():
    pass

