from typing import Any, Dict
from random import randint
from hypothesis import assume, event, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import wrappers_strategy


@settings(max_examples=100)
@given(wrappers=wrappers_strategy)
def test_remove_wrapper(wrappers: Dict[Uri, Any]):
    assume(wrappers)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.wrappers = {**wrappers}

    uris = list(wrappers.keys())
    uri_index = randint(0, len(uris) - 1)
    remove_uri = uris[uri_index]
    event(f"Uri to remove: {remove_uri}")

    builder.remove_wrapper(remove_uri)
    assert len(builder.config.wrappers) == len(wrappers) - 1
    assert remove_uri not in builder.config.wrappers


@settings(max_examples=100)
@given(wrappers=wrappers_strategy)
def test_remove_non_existent_wrapper(wrappers: Dict[Uri, Any]):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.wrappers = {**wrappers}

    builder.remove_wrapper(Uri("test", "non-existent"))
    assert builder.config.wrappers == wrappers


@settings(max_examples=100)
@given(wrappers=wrappers_strategy)
def test_remove_wrappers(wrappers: Dict[Uri, Any]):
    assume(wrappers)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.wrappers = {**wrappers}

    uris = list(wrappers.keys())
    uri_indices = [
        randint(0, len(uris) - 1) for _ in range(randint(0, len(uris) - 1))
    ]
    remove_uris = list({uris[uri_index] for uri_index in uri_indices})
    event(f"Uris to remove: {remove_uris}")

    builder.remove_wrappers(remove_uris)
    assert len(builder.config.wrappers) == len(wrappers) - len(remove_uris)
    assert set(remove_uris) & set(builder.config.wrappers.keys()) == set()


