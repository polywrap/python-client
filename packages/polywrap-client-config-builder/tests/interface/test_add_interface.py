from typing import Any, List
from hypothesis import given, settings, strategies as st

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import uri_strategy


@settings(max_examples=100)
@given(uri=uri_strategy, old_impls=st.lists(uri_strategy), new_impls=st.lists(uri_strategy))
def test_add_implementations_to_existing_interface(uri: Uri, old_impls: List[Uri], new_impls: List[Uri]):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.interfaces = {uri: old_impls}

    builder.add_interface_implementations(uri, new_impls)

    updated_impls = {*old_impls, *new_impls}

    assert set(builder.config.interfaces[uri]) == updated_impls


