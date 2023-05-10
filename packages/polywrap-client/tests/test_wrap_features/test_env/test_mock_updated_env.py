from typing import Callable

import pytest
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri

from polywrap_client import Env, InvokerOptions, PolywrapClient

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
async def test_mock_updated_env(
    implementation: str,
    builder: Callable[[str], ClientConfigBuilder],
    wrapper_uri: Callable[[str], Uri],
    expected_wrapper_env: Env,
):
    client = PolywrapClient(builder(implementation).build())
    override_env = {
        "object": {
            "prop": "object another string",
        },
        "str": "another string",
        "optFilledStr": "optional string",
        "number": 10,
        "bool": True,
        "en": "FIRST",
        "array": [32, 23],
    }
    mock_updated_env_result = await client.invoke(
        InvokerOptions(
            uri=wrapper_uri(implementation),
            method="methodRequireEnv",
            args={
                "arg": "string",
            },
            env=override_env,
        )
    )
    assert mock_updated_env_result == {**expected_wrapper_env, **override_env, "en": 0}
