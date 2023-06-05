from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_interface_invoke(
    implementation: str,
    builder: Callable[[str], ClientConfigBuilder],
    wrapper_uri: Callable[[str], Uri],
):
    client = PolywrapClient(builder(implementation).build())

    result = client.invoke(
        uri=wrapper_uri(implementation),
        method="moduleMethod",
        args={
            "arg": {
                "uint8": 1,
                "str": "Test String 1",
            },
        },
    )

    assert result == {
        "uint8": 1,
        "str": "Test String 1",
    }
