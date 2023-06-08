from typing import Any, Dict
from random import randint
from hypothesis import assume, event, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import envs_strategy


@settings(max_examples=100)
@given(envs=envs_strategy)
def test_remove_env(envs: Dict[Uri, Any]):
    assume(envs)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = {**envs}

    uris = list(envs.keys())
    uri_index = randint(0, len(uris) - 1)
    remove_uri = uris[uri_index]
    event(f"Uri to remove: {remove_uri}")

    builder.remove_env(remove_uri)
    assert len(builder.config.envs) == len(envs) - 1
    assert remove_uri not in builder.config.envs


@settings(max_examples=100)
@given(envs=envs_strategy)
def test_remove_non_existent_env(envs: Dict[Uri, Any]):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = {**envs}

    builder.remove_env(Uri("test", "non-existent"))
    assert builder.config.envs == envs


@settings(max_examples=100)
@given(envs=envs_strategy)
def test_remove_envs(envs: Dict[Uri, Any]):
    assume(envs)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = {**envs}

    uris = list(envs.keys())
    uri_indices = [
        randint(0, len(uris) - 1) for _ in range(randint(0, len(uris) - 1))
    ]
    remove_uris = list({uris[uri_index] for uri_index in uri_indices})
    event(f"Uris to remove: {remove_uris}")

    builder.remove_envs(remove_uris)
    assert len(builder.config.envs) == len(envs) - len(remove_uris)
    assert set(remove_uris) & set(builder.config.envs.keys()) == set()


