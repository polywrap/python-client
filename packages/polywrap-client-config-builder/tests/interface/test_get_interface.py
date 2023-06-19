from typing import Dict, List
from hypothesis import given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import interfaces_strategy


@settings(max_examples=100)
@given(interfaces=interfaces_strategy)
def test_get_interface_implementations(
    interfaces: Dict[Uri, List[Uri]]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.interfaces = interfaces

    for uri in interfaces:
        assert builder.get_interface_implementations(uri) == interfaces[uri]
    assert builder.get_interface_implementations(Uri.from_str("test/not-exists")) is None


def test_get_implementations_not_exists():
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_interface_implementations(Uri.from_str("test/not-exists")) is None


@settings(max_examples=100)
@given(interfaces=interfaces_strategy)
def test_get_interfaces(
    interfaces: Dict[Uri, List[Uri]]
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    assert builder.get_interfaces() == {}

    builder.config.interfaces = interfaces
    assert builder.get_interfaces() == interfaces
