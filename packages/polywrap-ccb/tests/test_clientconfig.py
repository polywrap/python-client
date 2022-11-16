import pytest
from polywrap_core import Uri, Env
from polywrap_ccb import ClientConfig, ClientConfigBuilder

def test_client_config_structure_starts_empty():
    ccb = ClientConfigBuilder()
    client_config = ccb.build()
    result = ClientConfig(envs={}, interfaces={}, resolver = None)
    assert client_config == result


def test_client_config_structure_sets_env():
    ccb = ClientConfigBuilder()
    uri = Uri("wrap://ens/eth.plugin.one"), 
    env = { 'color': "red", 'size': "small" }
    ccb = ccb.set_env(
        uri = uri, 
        env = env
        )
    client_config = ccb.build()
    assert client_config == ClientConfig(envs={uri: env}, interfaces={}, resolver = None)