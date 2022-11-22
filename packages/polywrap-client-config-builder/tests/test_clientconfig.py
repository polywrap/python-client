import pytest
from polywrap_core import Uri, Env
from polywrap_client_config_builder import ClientConfig, ClientConfigBuilder
from dataclasses import asdict

def test_client_config_structure_starts_empty():
    ccb = ClientConfigBuilder()
    client_config = ccb.build()
    result = ClientConfig(
        envs={},
        interfaces={}, 
        resolver = [],
        wrappers = []
        )
    assert asdict(client_config) == asdict(result)


def test_client_config_structure_sets_env():
    ccb = ClientConfigBuilder()
    uri = Uri("wrap://ens/eth.plugin.one"), 
    env = { 'color': "red", 'size': "small" }
    ccb = ccb.set_env(
        uri = uri, 
        env = env
        )
    client_config = ccb.build()
    assert asdict(client_config) == asdict(ClientConfig(envs={uri: env}, interfaces={}, resolver = [], wrappers=[]))

