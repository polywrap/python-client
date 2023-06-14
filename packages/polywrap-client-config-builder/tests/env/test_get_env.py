from typing import Any, Dict
from hypothesis import given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import envs_strategy


@settings(max_examples=100)
@given(envs=envs_strategy)
def test_get_env_exists(
    envs: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = envs

    for uri in envs:
        assert builder.get_env(uri) == envs[uri]
    assert builder.get_env(Uri.from_str("test/not-exists")) is None


def test_get_env_not_exists():
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_env(Uri.from_str("test/not-exists")) is None


@settings(max_examples=100)
@given(envs=envs_strategy)
def test_get_envs(
    envs: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_envs() == {}

    builder.config.envs = envs
    assert builder.get_envs() == envs
