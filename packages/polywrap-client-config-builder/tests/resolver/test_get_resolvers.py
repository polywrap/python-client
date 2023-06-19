from typing import List
from hypothesis import given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import UriResolver

from ..strategies import resolvers_strategy


@settings(max_examples=100)
@given(resolvers=resolvers_strategy)
def test_get_resolvers(
    resolvers: List[UriResolver]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_resolvers() == []

    builder.config.resolvers = resolvers
    assert builder.get_resolvers() == resolvers
