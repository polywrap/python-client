from typing import List
from hypothesis import given, settings, strategies as st

from polywrap_client_config_builder import (
    BuilderConfig,
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)

from .strategies import builder_config_strategy


@settings(max_examples=100)
@given(config=builder_config_strategy)
def test_add_builder_config(
    config: BuilderConfig,
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder = builder.add(config)
    assert builder.config.envs == config.envs
    assert builder.config.interfaces == config.interfaces
    assert builder.config.redirects == config.redirects
    assert builder.config.resolvers == config.resolvers
    assert builder.config.wrappers == config.wrappers
    assert builder.config.packages == config.packages


@settings(max_examples=10)
@given(configs=st.lists(builder_config_strategy, max_size=10))
def test_add_multiple_builder_config(configs: List[BuilderConfig]):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    expected_config = BuilderConfig()

    for config in configs:
        builder = builder.add(config)
        expected_config.envs.update(config.envs)
        expected_config.interfaces.update(config.interfaces)
        expected_config.packages.update(config.packages)
        expected_config.wrappers.update(config.wrappers)
        expected_config.redirects.update(config.redirects)
        expected_config.resolvers.extend(config.resolvers)

        assert builder.config == expected_config

    assert builder.config == expected_config


@settings(max_examples=100)
@given(config=builder_config_strategy)
def test_add_builder_config_with_duplicate_data(
    config: BuilderConfig,
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder = builder.add(config)
    builder = builder.add(config)
    assert builder.config.envs == config.envs
    assert builder.config.interfaces == config.interfaces
    assert builder.config.redirects == config.redirects
    assert len(builder.config.resolvers) == 2 * len(config.resolvers)
    assert builder.config.wrappers == config.wrappers
    assert builder.config.packages == config.packages
