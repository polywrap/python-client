from typing import Callable

import pytest
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri

from polywrap_client import Env, InvokerOptions, PolywrapClient

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
async def test_method_require_env(
    implementation: str,
    builder: Callable[[str], ClientConfigBuilder],
    wrapper_uri: Callable[[str], Uri],
    wrapper_env: Env,
    expected_wrapper_env: Env,
):
    client = PolywrapClient(builder(implementation).build())
    method_require_env_result = await client.invoke(
        InvokerOptions(
            uri=wrapper_uri(implementation),
            method="methodRequireEnv",
            args={
                "arg": "string",
            },
        )
    )
    assert method_require_env_result == expected_wrapper_env
