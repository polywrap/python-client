from typing import Any, Callable

import pytest
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri

from polywrap_client import PolywrapClient

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_subinvoke_env_method(
    implementation: str,
    builder: Callable[[str], ClientConfigBuilder],
    wrapper_uri: Callable[[str], Uri],
    expected_wrapper_env: Any,
    external_wrapper_env: Any,
):
    client = PolywrapClient(builder(implementation).build())
    subinvoke_env_method_result = client.invoke(
        uri=wrapper_uri(implementation),
        method="subinvokeEnvMethod",
        args={
            "arg": "string",
        },
    )
    assert subinvoke_env_method_result == {
        "local": expected_wrapper_env,
        "external": external_wrapper_env,
    }
