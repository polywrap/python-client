from typing import Any, Dict
from hypothesis import assume, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import envs_strategy, uri_strategy, env_strategy


@settings(max_examples=100)
@given(envs=envs_strategy, new_uri=uri_strategy, new_env=env_strategy)
def test_set_env(envs: Dict[Uri, Any], new_uri: Uri, new_env: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = {**envs}

    existing_uris = set(builder.config.envs.keys())
    assume(new_uri not in existing_uris)

    builder.set_env(new_uri, new_env)

    assert len(builder.config.envs) == len(existing_uris) + 1
    assert builder.config.envs[new_uri] == new_env


@settings(max_examples=100)
@given(uri=uri_strategy, old_env=env_strategy, new_env=env_strategy)
def test_set_env_overwrite(uri: Uri, old_env: Any, new_env: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = {uri: old_env}

    builder.set_env(uri, new_env)

    assert builder.config.envs == {uri: new_env}


@settings(max_examples=100)
@given(initial_envs=envs_strategy, new_envs=envs_strategy)
def test_set_envs(
    initial_envs: Dict[Uri, Any],
    new_envs: Dict[Uri, Any],
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = {**initial_envs}

    builder.set_envs(new_envs)

    assert len(builder.config.envs) <= len(initial_envs) + len(new_envs)
