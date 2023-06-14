from typing import Any, Dict
from hypothesis import assume, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import redirects_strategy, uri_strategy


@settings(max_examples=100)
@given(redirects=redirects_strategy, new_uri=uri_strategy, new_redirect=uri_strategy)
def test_set_redirect(redirects: Dict[Uri, Any], new_uri: Uri, new_redirect: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.redirects = {**redirects}

    existing_uris = set(builder.config.redirects.keys())
    assume(new_uri not in existing_uris)

    builder.set_redirect(new_uri, new_redirect)

    assert len(builder.config.redirects) == len(existing_uris) + 1
    assert builder.config.redirects[new_uri] == new_redirect


@settings(max_examples=100)
@given(uri=uri_strategy, old_redirect=uri_strategy, new_redirect=uri_strategy)
def test_set_env_overwrite(uri: Uri, old_redirect: Any, new_redirect: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.redirects = {uri: old_redirect}

    builder.set_redirect(uri, new_redirect)

    assert builder.config.redirects == {uri: new_redirect}


@settings(max_examples=100)
@given(initial_redirects=redirects_strategy, new_redirects=redirects_strategy)
def test_set_redirects(
    initial_redirects: Dict[Uri, Any],
    new_redirects: Dict[Uri, Any],
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.redirects = {**initial_redirects}

    builder.set_redirects(new_redirects)

    assert len(builder.config.envs) <= len(initial_redirects) + len(new_redirects)
