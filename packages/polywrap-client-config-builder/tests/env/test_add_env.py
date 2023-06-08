from typing import Any, Dict
from hypothesis import assume, given, settings

from polywrap_client_config_builder import (
    ClientConfigBuilder,
    PolywrapClientConfigBuilder,
)
from polywrap_core import Uri

from ..strategies import uri_strategy, env_strategy


@settings(max_examples=100)
@given(uri=uri_strategy, old_env=env_strategy, new_env=env_strategy)
def test_add_env(uri: Uri, old_env: Any, new_env: Any):
    builder: ClientConfigBuilder = PolywrapClientConfigBuilder()
    builder.config.envs = {uri: {"common": old_env, "unique_1": "unique_env_1"}}

    builder.add_env(uri, {"common": new_env, "unique_2": "unique_env_2"})

    updated_env = {**old_env, **new_env}

    assert builder.config.envs[uri] == {
        "common": updated_env,
        "unique_1": "unique_env_1",
        "unique_2": "unique_env_2",
    }
