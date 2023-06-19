from typing import Callable, Dict
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_client_config_builder.types import ClientConfigBuilder
import pytest

from ..consts import SUPPORTED_IMPLEMENTATIONS


@pytest.mark.parametrize("implementation", SUPPORTED_IMPLEMENTATIONS)
def test_bytes(
    implementation: str,
    builder: ClientConfigBuilder,
    wrapper_uri: Callable[[str, str], Uri],
):
    client = PolywrapClient(builder.build())
    uri = wrapper_uri("bytes-type", implementation)

    prop = b"hello world"
    expected = b"hello world Sanity!"

    response: bytes = client.invoke(
        uri=uri,
        method="bytesMethod",
        args={
            "arg": {
                "prop": prop,
            }
        },
    )

    assert response == expected

