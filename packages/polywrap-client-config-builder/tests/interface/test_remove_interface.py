from typing import Any, Dict, List
from random import randint
from hypothesis import assume, event, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import interfaces_strategy


@settings(max_examples=100)
@given(interfaces=interfaces_strategy)
def test_remove_interface(interfaces: Dict[Uri, List[Uri]]):
    assume(interfaces)
    assume(all(interfaces[interface] for interface in interfaces))
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.interfaces = {**interfaces}

    uris = list(interfaces.keys())
    uri_index = randint(0, len(uris) - 1)
    remove_uri = uris[uri_index]
    event(f"Uri to remove: {remove_uri}")

    builder.remove_interface(remove_uri)
    assert len(builder.config.interfaces) == len(interfaces) - 1
    assert remove_uri not in builder.config.interfaces


@settings(max_examples=100)
@given(interfaces=interfaces_strategy)
def test_remove_non_existent_interface(interfaces: Dict[Uri, List[Uri]]):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.interfaces = {**interfaces}

    builder.remove_interface(Uri("test", "non-existent"))
    assert builder.config.interfaces == interfaces


@settings(max_examples=100)
@given(interfaces=interfaces_strategy)
def test_remove_interface_implementations(interfaces: Dict[Uri, List[Uri]]):
    assume(interfaces)
    assume(all(interfaces[interface] for interface in interfaces))
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.interfaces = {**interfaces}

    uris = list(interfaces.keys())
    uri_index = randint(0, len(uris) - 1)
    remove_interface_uri = uris[uri_index]
    event(f"Interface Uri to remove: {remove_interface_uri}")

    impls_uris = list(interfaces[remove_interface_uri])
    impl_uri_indices = [
        randint(0, len(impls_uris) - 1) for _ in range(randint(0, len(impls_uris) - 1))
    ]
    remove_uris = list({impls_uris[uri_index] for uri_index in impl_uri_indices})
    event(f"Implementations Uri to remove: {remove_uris}")

    builder.remove_interface_implementations(remove_interface_uri, remove_uris)
    assert (
        set(remove_uris) & set(builder.config.interfaces[remove_interface_uri]) == set()
    )
