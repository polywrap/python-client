from typing import Any, Callable

import pytest
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri

from polywrap_client import PolywrapClient

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_method_require_env(
    implementation: str,
    builder: Callable[[str], ClientConfigBuilder],
    wrapper_uri: Callable[[str], Uri],
    wrapper_env: Any,
    expected_wrapper_env: Any,
):
    client = PolywrapClient(builder(implementation).build())
    method_require_env_result = client.invoke(
        uri=wrapper_uri(implementation),
        method="methodRequireEnv",
        args={
            "arg": "string",
        },
    )
    assert method_require_env_result == expected_wrapper_env

    k = {
        Uri(
            "file",
            "/Users/niraj/Documents/Projects/polywrap/python-client/packages/polywrap-test-cases/wrappers/env-type/01-main/implementations/rs",
        ): {
            "object": {"prop": "object string"},
            "str": "string",
            "optFilledStr": "optional string",
            "number": 10,
            "bool": True,
            "en": "FIRST",
            "array": [32, 23],
        },
        Uri(
            "file",
            "/Users/niraj/Documents/Projects/polywrap/python-client/packages/polywrap-test-cases/wrappers/env-type/00-external/implementations/rs",
        ): {"externalArray": [1, 2, 3], "externalString": "iamexternal"},
    }
