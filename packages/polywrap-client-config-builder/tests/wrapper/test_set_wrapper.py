from typing import Any, Dict
from hypothesis import assume, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import wrappers_strategy, uri_strategy, wrapper_strategy


@settings(max_examples=100)
@given(wrappers=wrappers_strategy, new_uri=uri_strategy, new_wrapper=wrapper_strategy)
def test_set_wrapper(wrappers: Dict[Uri, Any], new_uri: Uri, new_wrapper: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.wrappers = {**wrappers}

    existing_uris = set(builder.config.wrappers.keys())
    assume(new_uri not in existing_uris)

    builder.set_wrapper(new_uri, new_wrapper)

    assert len(builder.config.wrappers) == len(existing_uris) + 1
    assert builder.config.wrappers[new_uri] == new_wrapper


@settings(max_examples=100)
@given(uri=uri_strategy, old_wrapper=wrapper_strategy, new_wrapper=wrapper_strategy)
def test_set_env_overwrite(uri: Uri, old_wrapper: Any, new_wrapper: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.wrappers = {uri: old_wrapper}

    builder.set_wrapper(uri, new_wrapper)

    assert builder.config.wrappers == {uri: new_wrapper}


@settings(max_examples=100)
@given(initial_wrappers=wrappers_strategy, new_wrappers=wrappers_strategy)
def test_set_wrappers(
    initial_wrappers: Dict[Uri, Any],
    new_wrappers: Dict[Uri, Any],
):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.wrappers = {**initial_wrappers}

    builder.set_wrappers(new_wrappers)

    assert len(builder.config.envs) <= len(initial_wrappers) + len(new_wrappers)
