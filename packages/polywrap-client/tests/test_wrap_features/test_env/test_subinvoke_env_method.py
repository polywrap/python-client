from typing import Callable

import pytest
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri

from polywrap_client import Env, InvokerOptions, PolywrapClient

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
async def test_subinvoke_env_method(
    implementation: str,
    builder: Callable[[str], ClientConfigBuilder],
    wrapper_uri: Callable[[str], Uri],
    expected_wrapper_env: Env,
    external_wrapper_env: Env,
):
    client = PolywrapClient(builder(implementation).build())
    subinvoke_env_method_result = await client.invoke(
        InvokerOptions(
            uri=wrapper_uri(implementation),
            method="subinvokeEnvMethod",
            args={
                "arg": "string",
            },
        )
    )
    assert subinvoke_env_method_result == {
        "local": expected_wrapper_env,
        "external": external_wrapper_env,
    }
