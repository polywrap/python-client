from typing import Any, Dict
from random import randint
from hypothesis import assume, event, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import redirects_strategy


@settings(max_examples=100)
@given(redirects=redirects_strategy)
def test_remove_redirect(redirects: Dict[Uri, Any]):
    assume(redirects)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.redirects = {**redirects}

    uris = list(redirects.keys())
    uri_index = randint(0, len(uris) - 1)
    remove_uri = uris[uri_index]
    event(f"Uri to remove: {remove_uri}")

    builder.remove_redirect(remove_uri)
    assert len(builder.config.redirects) == len(redirects) - 1
    assert remove_uri not in builder.config.redirects


@settings(max_examples=100)
@given(redirects=redirects_strategy)
def test_remove_non_existent_redirect(redirects: Dict[Uri, Any]):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.redirects = {**redirects}

    builder.remove_redirect(Uri("test", "non-existent"))
    assert builder.config.redirects == redirects


@settings(max_examples=100)
@given(redirects=redirects_strategy)
def test_remove_redirects(redirects: Dict[Uri, Any]):
    assume(redirects)
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.redirects = {**redirects}

    uris = list(redirects.keys())
    uri_indices = [
        randint(0, len(uris) - 1) for _ in range(randint(0, len(uris) - 1))
    ]
    remove_uris = list({uris[uri_index] for uri_index in uri_indices})
    event(f"Uris to remove: {remove_uris}")

    builder.remove_redirects(remove_uris)
    assert len(builder.config.redirects) == len(redirects) - len(remove_uris)
    assert set(remove_uris) & set(builder.config.redirects.keys()) == set()


