from typing import Any, List
from hypothesis import given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import UriResolver

from ..strategies import resolvers_strategy, resolver_strategy


@settings(max_examples=100)
@given(resolvers=resolvers_strategy, new_resolver=resolver_strategy)
def test_add_resolver(resolvers: List[UriResolver], new_resolver: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.resolvers = [*resolvers]
    builder.add_resolver(new_resolver)

    assert len(builder.config.resolvers) == len(resolvers) + 1
    assert builder.config.resolvers[-1] == new_resolver


@settings(max_examples=100)
@given(initial_resolvers=resolvers_strategy, new_resolvers=resolvers_strategy)
def test_add_resolvers(
    initial_resolvers: List[UriResolver],
    new_resolvers: List[UriResolver],
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.resolvers = [*initial_resolvers]

    builder.add_resolvers(new_resolvers)

    assert len(builder.config.resolvers) == len(initial_resolvers) + len(new_resolvers)
