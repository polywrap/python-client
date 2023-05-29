from typing import Callable
from polywrap_client import PolywrapClient
from polywrap_client_config_builder.types import ClientConfigBuilder
from polywrap_core import Uri, InvokerOptions
import pytest

from ...consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
async def test_subinvoke(
    implementation: str,
    builder: Callable[[str], ClientConfigBuilder],
    wrapper_uri: Callable[[str], Uri],
):
    client = PolywrapClient(builder(implementation).build())

    result = await client.invoke(
        InvokerOptions(
            uri=wrapper_uri(implementation),
            method="addAndIncrement",
            args={"a": 1, "b": 1},
        )
    )

    assert result == 3
