from typing import Any, Dict
from hypothesis import given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import wrappers_strategy


@settings(max_examples=100)
@given(wrappers=wrappers_strategy)
def test_get_wrapper_exists(
    wrappers: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.wrappers = wrappers

    for uri in wrappers:
        assert builder.get_wrapper(uri) == wrappers[uri]
    assert builder.get_wrapper(Uri.from_str("test/not-exists")) is None


def test_get_wrapper_not_exists():
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_wrapper(Uri.from_str("test/not-exists")) is None


@settings(max_examples=100)
@given(wrappers=wrappers_strategy)
def test_get_wrappers(
    wrappers: Dict[Uri, Any]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_wrappers() == {}

    builder.config.wrappers = wrappers
    assert builder.get_wrappers() == wrappers
